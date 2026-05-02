"""Read-a-message prompt — TZ §3.1 Core 1."""
from __future__ import annotations

ANALYZE_MESSAGE_INSTRUCTION = """TASK: Read a single message from another person and report the forensic signals.

Required JSON keys (write the values in the OUTPUT LANGUAGE; keep the keys themselves in English):
{
  "actual_meaning": "What the sender actually means underneath the surface text. Subtext, not paraphrase.",
  "emotional_state": "Their emotional STATE in this moment — not a personality trait. One sentence.",
  "unsaid": ["Conspicuous absences — what they could have said but didn't. List as specific phrases."],
  "desired_response_real": "What they actually want from you, behaviorally.",
  "desired_response_stated": "What they say they want — may differ from above.",
  "recommended_action": "ONE OF: reply_now | wait | ask_clarifying_question | let_it_go | escalate_to_call",
  "confidence": "ONE OF: high | medium | low",
  "confidence_reason": "Plain reason. If low, name the missing data the user would need to bring."
}

If reverse_mode is True (you'll see it in the input block), ALSO produce:
{
  "alternative_phrasings": [
    {"label": "firmer", "text": "...", "explanation": "linguistic choice + predicted reception"},
    {"label": "warmer", "text": "...", "explanation": "..."},
    {"label": "more_strategic", "text": "...", "explanation": "..."}
  ]
}

Rules:
- One message ≠ a pattern. Default confidence is "low" or "medium" unless the linguistic structure makes the signal unambiguous.
- Cite specific words, sentence structures, or pacing where possible.
- Never recommend a specific therapy, legal, or medical action.
- If the message contains crisis language, keep your analysis but stay sober — the system will attach localized resources separately.
"""


def build_analyze_message_prompt(
    *,
    message_text: str,
    relationship_context: str | None,
    spotlight_prompt: str,
    reverse_mode: bool,
) -> str:
    parts: list[str] = [
        ANALYZE_MESSAGE_INSTRUCTION,
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
    ]
    if relationship_context:
        parts.append(f"RELATIONSHIP CONTEXT (from user): {relationship_context.strip()}")
        parts.append("")
    parts.append(f"REVERSE MODE: {'true' if reverse_mode else 'false'}")
    parts.append("")
    parts.append("MESSAGE TO ANALYZE (verbatim, do not modify):")
    parts.append("---BEGIN MESSAGE---")
    parts.append(message_text.strip())
    parts.append("---END MESSAGE---")
    parts.append("")
    parts.append("Return ONLY a single JSON object matching the schema above. No prose, no markdown.")
    return "\n".join(parts)
