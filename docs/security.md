# DevLink Security Documentation

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
