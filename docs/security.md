# DevLink Security Documentation

## Password Screening (#855)

Composition rules alone are a weak defence. `Password1!`, `Welcome123!` and
`Qwerty123!` all satisfy "8 characters, upper, lower, digit, symbol" and all
appear near the top of every credential-stuffing wordlist. NIST SP 800-63B
recommends screening candidate passwords against known-bad values rather than
relying on composition, so `validate_password` now runs three additional checks
after the structural ones.

### 1. Local blocklist

`app/core/password_blocklist.py` holds an in-repo list of the most commonly
observed passwords. Candidates are normalised before comparison:

| Input             | Normalised | Rejected |
| :---------------- | :--------- | :------- |
| `password`        | `password` | yes      |
| `P@ssw0rd`        | `password` | yes      |
| `Password2025!`   | `password` | yes      |
| `Welcome123!`     | `welcome`  | yes      |

Normalisation lowercases, applies Unicode NFKD folding, strips trailing digits
and punctuation, then undoes common leetspeak substitutions. That means one
blocklist entry covers a whole family of decorated variants, so the list stays
small enough to read.

### 2. Personal information

A password that contains the user's own username or email local-part is
rejected. `alexrivera` picking `Alex.Rivera2025!` is on the first page of any
targeted guess list. Tokens shorter than four characters are ignored — a short
identifier would otherwise match nearly everything — and the email *domain* is
not considered, since every user shares it.

### 3. Have I Been Pwned

The long tail is covered by the HIBP range API using k-anonymity:

1. SHA-1 the candidate password.
2. Send **only the first five hex characters** of the digest.
3. HIBP returns every suffix it holds under that prefix — several hundred.
4. Match our suffix against that list locally.

The password never leaves the process, and neither does its full hash. Requests
set `Add-Padding: true` so every response contains a similar number of entries
and an observer cannot infer anything from the response size. Range responses
are cached for 24 hours.

**This check fails open.** A timeout, connection error or 5xx from HIBP is
logged and treated as "no reason to reject". An outage at a third party must
never become an outage of our signup form.

### Where it applies

Registration, password change, and password reset. Each passes the account's
username and email so the personal-information check has context.

### Configuration

| Setting                     | Default                              | Purpose                                            |
| :-------------------------- | :----------------------------------- | :------------------------------------------------- |
| `ENABLE_PASSWORD_BLOCKLIST` | `true`                               | Local blocklist and personal-information checks     |
| `ENABLE_HIBP_CHECK`         | `true` (`false` under pytest)        | HIBP range lookup                                   |
| `HIBP_API_URL`              | `https://api.pwnedpasswords.com/range` | Range API endpoint                                |
| `HIBP_TIMEOUT_SECONDS`      | `3.0`                                | Per-request timeout                                 |
| `HIBP_MIN_BREACH_COUNT`     | `5`                                  | Occurrences before a password is rejected           |
| `HIBP_CACHE_TTL_SECONDS`    | `86400`                              | How long a range response is cached                 |

`HIBP_MIN_BREACH_COUNT` is above 1 deliberately: single-occurrence entries in
the corpus are often artefacts rather than passwords in active circulation.

`ENABLE_HIBP_CHECK` defaults off under pytest so the suite never depends on a
third party being reachable; the behaviour itself is covered with a mocked
transport in `tests/test_password_screening.py`.

### Error messages

Rejection messages state the category ("too common", "appeared in a known data
breach") and never echo the submitted password back to the client.

---

## Suspicious Login Detection System (#584)

DevLink evaluates all authentication attempts (both successful and failed) in real time to detect suspicious login patterns and protect user accounts against unauthorized access, credential stuffing, and brute force attacks.

### Detection Signals

1. **New Device (`NEW_DEVICE`)**:
   - Compares the client user-agent / device type against historical successful logins recorded for the user in the past 30 days.

2. **New Browser (`NEW_BROWSER`)**:
   - Evaluates the browser family (Chrome, Firefox, Safari, Edge, etc.) against known browsers previously used by the account holder.

3. **Unusual Location (`UNUSUAL_LOCATION`)**:
   - Detects login attempts from IP addresses that differ from the user's past 30-day login history.

4. **Multiple Failed Logins (`MULTIPLE_FAILED_LOGINS`)**:
   - Triggers when 3 or more failed password authentication attempts occur within a 15-minute window for a specific account or IP address.

5. **Rapid Login Attempts (`RAPID_LOGIN_ATTEMPTS`)**:
   - Flags accounts experiencing 2 or more login attempts within a 5-second window.

### Automated Responses

- **Security Alert Notification**: Immediately generates an urgent in-app/email security alert to the user detailing the login attempt, client IP, device info, and triggered detection signals.
- **Immutable Audit Logging**: Records an immutable audit log entry (`AuditAction.SUSPICIOUS_LOGIN_ATTEMPT`) with full request context metadata for security auditing.
