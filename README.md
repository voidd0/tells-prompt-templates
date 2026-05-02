# tells-prompt-templates

> Public copy of every system prompt that [tells](https://tells.voiddo.com) sends to Google Gemini.

This repository exists so you can verify, exactly, what the AI behind tells
sees when you submit a message, profile excerpt, or draft. Nothing in this
repo is a marketing description; it's the actual production prompt
templates, copied here verbatim from the (private) tells backend.

The implementation that wires these prompts together — request handling,
authentication, billing, persistence — stays in the private backend. This
repo is the prompt layer alone.

## Why publish

We split the privacy surface from the business surface:

- **Public** — security primitives, prompt templates, cultural framing files.
- **Private** — backend application code, database schemas, business logic.

The three public privacy components:

- [voidd0/tells-encryption-spec](https://github.com/voidd0/tells-encryption-spec) — the AES-256-GCM + HKDF + AAD spec.
- [voidd0/tells-prompt-templates](https://github.com/voidd0/tells-prompt-templates) — this repo.
- [voidd0/tells-cultural-framing](https://github.com/voidd0/tells-cultural-framing) — per-language framing layer.

## What's in this repo

### Top-level prompts

- [`base.py`](base.py) — the shared system-prompt scaffolding (forensic
  framing, refusal rules, output discipline).
- [`analyze_message.py`](analyze_message.py) — the read-a-message prompt
  (single-message analysis, the most-used surface).
- [`analyze_person.py`](analyze_person.py) — the read-a-person prompt
  (multi-message corpus analysis for one tracked person).
- [`analyze_profile.py`](analyze_profile.py) — the read-a-profile prompt
  (dating-app or social-profile analysis).
- [`mirror.py`](mirror.py) — the Mirror prompt (analyses the user's own
  writing samples for self-knowledge).
- [`voice_coach.py`](voice_coach.py) — the Voice Coach prompt (rewrites a
  draft message in three alternative phrasings).
- [`decisions.py`](decisions.py) — the Decisions prompt (helps the user
  think through a relational decision).
- [`voice_adjustments.py`](voice_adjustments.py) — per-language voice
  register adjustments (formal/informal/direct).

### Subdirectories

- [`cultural_framing/`](cultural_framing/) — the 12 per-language framing
  files that adjust tone, directness, family-hierarchy sensitivity,
  manipulation-terminology caution, and metaphor preferences. EN / DE / FR /
  ES / PT-BR / JA / KO / IT / TR / RU / AR / HE.
  - This subdirectory is also published standalone at
    [voidd0/tells-cultural-framing](https://github.com/voidd0/tells-cultural-framing)
    so the community can contribute corrections without needing to read the
    full prompt layer.
- [`profile_platforms/`](profile_platforms/) — platform-specific framing
  for read-a-profile mode. Bumble / Hinge / Instagram / LinkedIn / Reddit /
  TikTok / Tinder / X / generic.
- [`spotlights/`](spotlights/) — the 8 onboarding spotlights that adjust
  the analysis lens at request time. Conflict / Dating / Family / Friendship
  / Patterns / Public-figure / Self / Workplace.

## What Gemini receives per request

For each analysis call, Gemini receives:

1. The system prompt for the requested mode (one of the top-level files above).
2. The cultural framing JSON for the user's selected language.
3. The relevant spotlight framing.
4. The text content the user submitted, verbatim.
5. A response schema (so the output is structured JSON we can validate).

Gemini does **not** receive: the user's email, IP, account ID, tracked-person
labels, billing tier, signup date, or any cross-request identifier. Each call
is stateless. We use Gemini under enterprise data-protection terms — content
is not used for model training.

## Versioning

This repo is versioned alongside the production backend. Material prompt
changes (anything that affects what Gemini sees, not just typo fixes) are
committed here within 24 hours of going live in production.

The diff history of this repo is the canonical record of what tells has ever
asked Gemini.

## Reporting issues

If you find:

- A prompt that asks Gemini for something we did not document publicly,
- A factual error in a cultural-framing file,
- A platform-specific framing that misrepresents the platform,

— open an issue or email [hi@voiddo.com](mailto:hi@voiddo.com). Cultural
framing PRs from native speakers are especially welcome (see also the
standalone [tells-cultural-framing](https://github.com/voidd0/tells-cultural-framing)
repo).

## License

MIT — see [LICENSE](LICENSE).

---

Built by [vøiddo](https://voiddo.com/) — a small studio shipping AI-flavoured products, free dev tools, Chrome extensions and weird browser games.
