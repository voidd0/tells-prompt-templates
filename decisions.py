"""Lightweight decisions prompt — TZ §3.2 (Pro skill).

Pro+ only. Takes a relational decision question + 2-N options + a thinking
lens (pros/cons, long-term/short-term, second-order effects, reverse brainstorm).

Returns per-option analysis + a recommended option + reasoning. NEVER tells
the user what to do — frames trade-offs.
"""
from __future__ import annotations


LENS_DESCRIPTIONS: dict[str, str] = {
    "pros_cons": (
        "Lens: Pros and Cons.\n"
        "For each option, list what it actively gains and what it actively costs. "
        "Surface trade-offs honestly. Do not pad either column."
    ),
    "long_term_short_term": (
        "Lens: Long-term vs Short-term.\n"
        "For each option, separate immediate consequences (next 1-4 weeks) from durable consequences (6-24 months). "
        "Flag where short-term comfort costs long-term capacity, and vice versa."
    ),
    "second_order_effects": (
        "Lens: Second-order effects.\n"
        "For each option, walk: first-order = direct consequence; second-order = downstream consequence enabled by the first; "
        "third-order = the consequence of the second that's hard to see now. Surface the third-order specifically."
    ),
    "reverse_brainstorm": (
        "Lens: Reverse brainstorm.\n"
        "For each option, ask: 'How would I make this option fail?' "
        "List 3-5 ways. Then re-evaluate the option once those failure modes are visible."
    ),
}


DECISIONS_INSTRUCTION = """TASK: Help the user think through a relational decision. NEVER tell them what to do — surface trade-offs.

Required JSON shape (write VALUES in the OUTPUT LANGUAGE; keep KEYS in English):
{
  "lens_used": "echo the lens slug used (pros_cons | long_term_short_term | second_order_effects | reverse_brainstorm)",
  "per_option_analysis": [
    {
      "option": "verbatim option text from user",
      "analysis": "lens-shaped analysis of this option — concrete, no padding",
      "key_risks": ["specific risks for this option"],
      "key_upsides": ["specific upsides for this option"]
    }
  ],
  "comparative_summary": "1-2 sentence summary of how the options actually differ on what matters",
  "recommended_option": "verbatim option text the analysis points toward — or 'no recommendation' if the trade-offs are roughly even",
  "recommended_option_reason": "if recommended, why; if not, why the trade-offs are too even to recommend",
  "decision_blockers": ["if applicable: information the user doesn't yet have that would change the analysis"],
  "confidence": "high | medium | low"
}

Hard requirements:
- per_option_analysis must contain one entry per option (in input order).
- Never moralize the user's options.
- Never recommend therapy, legal, or medical action.
- 'recommended_option' MUST be a verbatim string from the user's options OR exactly 'no recommendation'.
"""


def build_decisions_prompt(
    *,
    decision_question: str,
    options: list[str],
    lens: str,
    target_block: str | None,
    spotlight_prompt: str,
) -> str:
    lens_desc = LENS_DESCRIPTIONS.get(lens, LENS_DESCRIPTIONS["pros_cons"])
    parts: list[str] = [
        DECISIONS_INSTRUCTION,
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
        lens_desc,
        "",
        f"DECISION QUESTION: {decision_question.strip()}",
        "",
        "OPTIONS:",
    ]
    for i, opt in enumerate(options, start=1):
        parts.append(f"  {i}. {opt.strip()}")
    parts.append("")
    if target_block:
        parts.append(f"TRACKED PERSON CONTEXT (use to inform analysis):\n{target_block.strip()}")
        parts.append("")
    parts.append("Return ONLY a single JSON object matching the schema above. No prose, no markdown.")
    return "\n".join(parts)
