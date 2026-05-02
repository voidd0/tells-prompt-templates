"""Read-a-person prompt — TZ §3.1 Core 2.

Forensic profile from a corpus of messages. The model is asked to cite
specific excerpts with timestamps verbatim from the input and emit confidence
ratings per section, never globally averaged.
"""
from __future__ import annotations

from typing import Iterable


ANALYZE_PERSON_INSTRUCTION = """TASK: Read a person across many messages and emit a forensic profile.

You are given a corpus of messages this person sent (direction: 'in' = from them,
'out' = from the user). Treat 'in' messages as primary evidence; treat 'out' as
context for what the person was responding to.

Required JSON shape (write VALUES in the OUTPUT LANGUAGE; keep KEYS in English):
{
  "attachment_style": "secure | anxious | avoidant | disorganized — and why, in one sentence anchored to corpus features",
  "communication_pattern": "their characteristic rhythm: response latency, length skew, topic-evasion, repair behavior, escalation curve",
  "manipulation_markers": [
    {"type": "DARVO | gaslighting | guilt_trip | love_bombing | silent_treatment | triangulation | other",
     "evidence_excerpt": "verbatim from input",
     "timestamp": "ISO from input"}
  ],
  "power_dynamics": "who centres the relational frame, how disagreements end, who concedes",
  "emotional_volatility_index": "low | medium | high — score with one-sentence reason from corpus features",
  "consistency_score": "low | medium | high — how much their stated values match observed behavior across the corpus",
  "recurring_themes": ["theme 1", "theme 2", "..."],
  "unresolved_threads": ["topic the person dropped without resolution", "..."],
  "cited_excerpts": [
    {"text": "verbatim quote from input",
     "timestamp": "ISO from input",
     "section_referenced": "which output section this supports (e.g. 'manipulation_markers')",
     "confidence": "high | medium | low"}
  ],
  "confidence_ratings": {
    "attachment_style": "high | medium | low",
    "communication_pattern": "high | medium | low",
    "manipulation_markers": "high | medium | low",
    "power_dynamics": "high | medium | low",
    "emotional_volatility_index": "high | medium | low",
    "consistency_score": "high | medium | low"
  },
  "recommended_orientation": "How the user might calibrate going forward. Forensic, not therapeutic. One paragraph max.",
  "crisis_flag": false
}

Rules:
- Cite VERBATIM. Never paraphrase a quoted excerpt.
- Use the exact timestamp string as it appears in the input.
- A corpus shorter than 8 messages cannot support 'high' confidence — cap each section at 'medium'.
- A corpus shorter than 3 messages caps every section at 'low' and limits manipulation_markers to [].
- If the corpus contains crisis language, set crisis_flag=true; the surrounding system attaches localized resources.
- Never recommend therapy / legal action / specific medical steps.
- Never moralize. Describe signals, not character verdicts.
"""


def _serialize_corpus(messages: Iterable[dict]) -> str:
    """Serialize the messages array as a compact, model-friendly transcript.

    Each line: `[<timestamp>] <DIR> <text>`. We include a header so the model
    knows what 'in' / 'out' mean in this run.
    """
    lines: list[str] = [
        "CORPUS LEGEND: 'in' = message FROM the analyzed person, 'out' = message FROM the user.",
        "Treat 'in' as primary evidence. Cite timestamps verbatim from the lines below.",
        "",
    ]
    for m in messages:
        ts = str(m.get("timestamp", "")).strip()
        direction = str(m.get("direction", "in")).strip().lower()
        text = str(m.get("text", "")).strip().replace("\n", " ")
        lines.append(f"[{ts}] {direction.upper()} {text}")
    return "\n".join(lines)


def build_analyze_person_prompt(
    *,
    messages_corpus: list[dict],
    spotlight_prompt: str,
    period_start: str | None,
    period_end: str | None,
    relationship_context: str | None = None,
) -> str:
    parts: list[str] = [
        ANALYZE_PERSON_INSTRUCTION,
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
    ]
    if period_start or period_end:
        parts.append(
            f"OBSERVATION PERIOD: {period_start or 'unknown start'} → {period_end or 'unknown end'}"
        )
        parts.append("")
    if relationship_context:
        parts.append(f"RELATIONSHIP CONTEXT (from user): {relationship_context.strip()}")
        parts.append("")
    parts.append(f"CORPUS LENGTH: {len(messages_corpus)} messages")
    parts.append("")
    parts.append("---BEGIN CORPUS---")
    parts.append(_serialize_corpus(messages_corpus))
    parts.append("---END CORPUS---")
    parts.append("")
    parts.append("Return ONLY a single JSON object matching the schema above. No prose, no markdown.")
    return "\n".join(parts)
