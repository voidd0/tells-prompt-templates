"""Voice coach prompt — TZ §3.2.

User has a draft they want to send. We:
1. Read what the draft actually conveys vs intends.
2. Generate 3 alternative phrasings (always 3 — the offering is the choice).
3. If a tracked person's pattern is loaded, predict their reception of each variant.
4. Recommend one with confidence + reasoning.
"""
from __future__ import annotations


VOICE_COACH_INSTRUCTION = """TASK: Read a draft message the user is about to send. Critique what it actually conveys vs what they intend, then offer 3 alternative phrasings calibrated to a tone target.

Required JSON shape (write VALUES in the OUTPUT LANGUAGE; keep KEYS in English):
{
  "original_assessment": {
    "what_it_conveys": "what a careful reader will actually take away",
    "what_it_intends": "what the user wants to convey (per relationship_context + desired_outcome)",
    "gap": "the delta between conveys and intends — be specific",
    "predicted_reception": "if recipient pattern is provided, how THEY will read it; otherwise a generic predicted reception"
  },
  "alternative_phrasings": [
    {
      "text": "the rewritten message in its entirety, ready to send",
      "approach": "label for the rewrite strategy (e.g. 'firmer', 'warmer', 'more strategic', 'shorter', 'reframed')",
      "tradeoffs": "what this version gains, what it gives up",
      "predicted_target_response": "if recipient pattern is provided, predicted response; otherwise a generic predicted reception"
    }
  ],
  "recommended_choice": 0,
  "recommended_choice_reason": "why this option, given the tone_target and desired_outcome",
  "confidence": "high | medium | low"
}

Hard requirements:
- alternative_phrasings MUST contain EXACTLY 3 entries.
- recommended_choice MUST be an integer 0, 1, or 2 — index into alternative_phrasings.
- Each phrasing must be a complete message, ready to copy-send. Not a fragment.
- Do not write generic templates ("hi {{name}}, ..."). Use the actual context.
- Match the tone_target. If it's "warm", the variants should differ in warmth, not in being un-warm.
- Never advise crossing a stated boundary (e.g. don't propose ignoring a no).
- Never moralize the user's intent. Help them say what they want better.
"""


def _serialize_target_context(target_block: str | None) -> str:
    if not target_block:
        return "TARGET PERSON CONTEXT: not loaded — make generic predictions of reception."
    return f"TARGET PERSON CONTEXT (from prior pattern snapshot — use to predict reception):\n{target_block.strip()}"


def build_voice_coach_prompt(
    *,
    draft_text: str,
    relationship_context: str | None,
    desired_outcome: str,
    tone_target: str,
    target_block: str | None,
    spotlight_prompt: str,
) -> str:
    parts: list[str] = [
        VOICE_COACH_INSTRUCTION,
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
        f"TONE TARGET: {tone_target}",
        f"DESIRED OUTCOME: {desired_outcome.strip()}",
    ]
    if relationship_context:
        parts.append(f"RELATIONSHIP CONTEXT: {relationship_context.strip()}")
    parts.append("")
    parts.append(_serialize_target_context(target_block))
    parts.append("")
    parts.append("---BEGIN DRAFT---")
    parts.append(draft_text.strip())
    parts.append("---END DRAFT---")
    parts.append("")
    parts.append("Return ONLY a single JSON object matching the schema above. No prose, no markdown.")
    return "\n".join(parts)
