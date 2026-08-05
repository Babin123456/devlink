# Content Moderation

DevLink accepts free text in a lot of places — messages, project descriptions,
conversation starters, feedback, profile bios, issue comments — and until now
none of it was screened. There is a `UserReport` model, so the design was
entirely reactive: something abusive gets posted, somebody reads it, somebody
reports it, a moderator eventually acts.

This adds the deterministic layer that runs *before* the write.

## It returns a recommendation, not a verdict

```python
from app.services.moderation_service import moderation_service, Action

result = moderation_service.check(message_body)

if result.action == Action.BLOCK:
    raise HTTPException(400, detail=result.explain())
```

| Action | Meaning |
| --- | --- |
| `allow` | Nothing interesting. |
| `flag` | Publish it, but queue it for review. |
| `review` | Hold it; a moderator decides. |
| `block` | Refuse it, and tell the author why. |

The **caller** decides what to do with the recommendation. A profile bio and a
direct message should not share a threshold, and that is a property of the call
site, not of the text. Pass your own `thresholds` to move the line.

## Every result explains itself

```python
result.signals
# [Signal(category=SPAM, rule='url_shortener', weight=0.4, detail='bit.ly'),
#  Signal(category=SPAM, rule='spam_phrase', weight=0.3, detail='guaranteed returns')]

result.explain()
# "review @ 0.70: url_shortener (+0.40), spam_phrase (+0.30)"
```

This is not decoration. A moderation decision nobody can explain is a decision
nobody can appeal, and somebody will eventually have to answer a *"why was my
post blocked"* ticket. The signal list is what makes that answerable.

## Normalisation, and the trap in it

A check written as `term in text.lower()` is defeated by every evasion anybody
has ever tried:

| Evasion | Mechanism |
| --- | --- |
| `f u c k` | spacing |
| `f.u.c.k` | separators |
| `fvck`, `sh1t`, `a$$hole` | substitution |
| `fυck` | Greek upsilon rendering as a "u" |
| `𝐟𝐮𝐜𝐤` | mathematical bold — a different codepoint per letter |
| `fuuuuuck` | repetition |

The obvious fix is to strip everything — spaces, punctuation, digits — into one
blob and substring-match against that. **Do not do this.** With the separators
gone:

* `Scunthorpe` contains a swear word
* `class` contains a slur
* `assignment` contains a swear word

That is the Scunthorpe problem, and every filter that ships without a test for
it eventually ships the bug.

So `app/utils/text_normalize.py` splits the difference:

* **`normalise()`** is the safe fold. Accents, script homoglyphs (Cyrillic,
  Greek) and repeated characters are dealt with; separators become single
  spaces so **word boundaries survive**. Digits and symbols are left alone,
  because `123` is a number and `!` is punctuation. This is what whole-word
  matching runs against.
* **`evasion_pattern(term)`** builds a per-term regex that tolerates
  separators and substitutions *inside* the term — `f+[sep]{0,2}[uv]+…` — while
  still requiring a word boundary around the **whole match**.

That asymmetry is the entire design. `c u n t` matches; `Scunthorpe` does not,
because the lookbehind sees the `s`.

`squash()` still exists for comparing two strings that should be the same word,
and its docstring says in as many words that it is not safe to substring-match
a term list against.

### Known limit

Substitutions come from a table. An unusual one — `f4ck`, where the `4` stands
for a `u` rather than the `a` it normally spells — is missed. That is an
accepted limit of a deterministic layer: the fix is to add the mapping, not to
loosen the pattern until it starts eating ordinary words.

## Signals

**Abuse**

| Rule | Weight | Notes |
| --- | --- | --- |
| `profanity` | 0.30–0.60 | A **flag**, not a block. A developer platform that refuses "this API is a shitshow" is a platform nobody uses. |
| `slur` | 1.00 | Blocks. |
| `harassment` | 1.00 | Blocks. Phrases aimed at a person, not a situation. |
| `obfuscated_term` | 0.35 | Scored below a plain hit: obfuscation is evidence of intent, but the pattern is looser than an exact match. |

**Spam**

| Rule | Weight | Notes |
| --- | --- | --- |
| `link_density` | 0.20–0.60 | Relative to length. Three links in a paragraph is a well-referenced paragraph; three links in fifteen words is a drop. `ALLOWED_DOMAINS` (GitHub, MDN, PyPI…) never count. |
| `url_shortener` | 0.40 each | A shortener hides its destination, which is the whole reason it is there. |
| `spam_phrase` | 0.30–0.90 | |
| `solicited_contact_details` | 0.50 | Contact-soliciting language **and** an email or phone number. |
| `offsite_contact_request` | 0.25 | The language without the details. An email in a bug report is just an email. |

**Formatting** — `excessive_caps` (0.20), `character_repetition` (0.15),
`word_repetition` (0.25). Weak individually; somebody is allowed to be excited.
They earn their place as tiebreakers because they correlate with everything
else on the list.

## Author context

```python
moderation_service.check(text, author=AuthorContext(
    account_age_days=0, prior_flags=2, is_verified=False,
))
```

A brand-new account posting five links is not the same event as a two-year-old
account doing it, and no amount of keyword matching can tell those apart.

| Signal | Multiplier |
| --- | --- |
| Account < 1 day | ×1.5 |
| Account < 7 days | ×1.25 |
| Account > 1 year | ×0.8 |
| ≥ 3 prior flags | ×1.4 |
| ≥ 1 prior flag | ×1.15 |
| Verified | ×0.7 |

Two deliberate details:

1. The multiplier is only applied when something already fired. Multiplying
   zero is pointless, and a new account posting something clean must still
   score zero.
2. **The age discount does not apply to slurs or harassment.** Seniority is not
   a licence.

## Extending the lists

Terms live in `app/core/moderation_terms.py`, which is pure data. Add a term in
ordinary spelling and the service handles the evasions — there is no need to
enumerate `f4ck`, `fυck` and `f.u.c.k`.

The `SLURS` list in the repository is deliberately short and non-exhaustive.
Deployments are expected to extend it; the scoring code does not change when
they do.

## What this is not

No ML model, no third-party moderation API. This is the layer that runs on
every submission in under a millisecond, is explainable, and can be unit-tested
against *"does Scunthorpe still work"*. A model can sit behind it later, for
the cases rules cannot reach — but a model cannot answer that question, which
is why it is not the first layer.

## The preview endpoint

```
POST /api/moderation/check   { "text": "…", "account_age_days": 3 }
```

Authenticated, rate limited to 60/minute. It exists so the frontend can warn
somebody *before* they hit send — far better than a rejection afterwards — and
so moderators can check why a particular piece of text scored the way it did
without reading the source. It returns nothing about anybody else.
