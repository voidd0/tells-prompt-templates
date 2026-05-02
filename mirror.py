"""Mirror-mode prompt — TZ §3.2.

User analyzing themselves. Same forensic shape as person/profile but with two
mandatory additions: strengths (3-5, with cited evidence) and growth_orientations
(3-5, never framed as 'fixes' or 'deficits').

Brutal honesty without softening — but strengths section appears FIRST in
the rendered output to keep the experience truthful, not punishing.
"""
from __future__ import annotations


MIRROR_INSTRUCTION = """TASK: Read the user's own writing (or their own profile) back to them.

The user has confirmed (self_aware = true) that the input is THEIR OWN writing or
profile. Be honest in a way that is useful — no softening, no therapy-speak,
no false validation. But ALSO no punishment. Forensic mirror, not roast.

Required JSON shape (write VALUES in the OUTPUT LANGUAGE; keep KEYS in English):
{
  "strengths": [
    {"trait": "specific honest positive trait or capability",
     "evidence_excerpt": "verbatim from the input that supports this",
     "confidence": "high | medium | low"}
  ],
  "growth_orientations": [
    {"orientation": "direction the user could grow into — never framed as 'fix this' or 'you lack X'",
     "evidence_excerpt": "what in the input prompts this",
     "confidence": "high | medium | low"}
  ],
  "patterns_observed": ["recurring move, habit, or rhythm"],
  "self_image_vs_text": "how the user appears to see themselves vs how the text reads them",
  "blind_spots": ["specific things visible to a reader that the writer may not see"],
  "voice_signature": "what's distinctive about how they sound (could be strength or risk)",
  "default_modes": "which emotional registers they default to under pressure",
  "register_with_others": "if conversational input — how they tend to position themselves in a relational frame",
  "confidence_overall": "high | medium | low",
  "crisis_flag": false
}

Hard requirements:
- 'strengths' MUST contain at least 3 entries. Mirrors that fail to find strengths are punishment, not analysis.
- 'growth_orientations' MUST contain at least 3 entries.
- Never use the words 'fix', 'broken', 'wrong with you', or therapy-clichés.
- Cite verbatim where possible.
- If the input contains crisis content, set crisis_flag=true.
"""


def build_mirror_prompt(
    *,
    mode: str,
    payload_block: str,
    spotlight_prompt: str,
) -> str:
    parts: list[str] = [
        MIRROR_INSTRUCTION,
        "",
        f"MIRROR MODE: {mode}  (person = corpus of own messages; profile = own profile)",
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
        "---BEGIN INPUT---",
        payload_block.strip(),
        "---END INPUT---",
        "",
        "Return ONLY a single JSON object matching the schema above. No prose, no markdown.",
    ]
    return "\n".join(parts)
