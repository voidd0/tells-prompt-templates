"""Read-a-profile prompt — TZ §3.1 Core 3.

Decodes a public/social profile (LinkedIn / X / Hinge / etc) into:
- presented_self vs between_lines
- inconsistencies + gaps
- signaling layer (status / aspiration / insecurity)
- inferred traits with confidence
- red/green flags
- platform-conditional recommendations (first-message angle for dating; outreach angle for LinkedIn)
"""
from __future__ import annotations


ANALYZE_PROFILE_INSTRUCTION = """TASK: Decode a profile from a public/social platform.

You receive scraped or pasted profile text. Return a forensic profile reading.

Required JSON shape (write VALUES in the OUTPUT LANGUAGE; keep KEYS in English):
{
  "presented_self": "What the profile is actively SAYING about who they are. The official version.",
  "between_lines": "What the profile is doing OTHER than what it claims — subtext, pose, deflection.",
  "inconsistencies": ["specific contradictions between sections / claims / activity / aesthetic"],
  "gaps_noted": ["conspicuous absences — what a similar profile would normally say but this one doesn't"],
  "signaling_layer": {
    "status_signals": ["evidence the profile is positioning for status, where, and to whom"],
    "aspiration_signals": ["evidence of who they want to be (vs are)"],
    "insecurity_signals": ["evidence of which judgments they're pre-emptively defending against"],
    "social_positioning": "which audience the profile recruits — and which it filters out"
  },
  "inferred_traits": [
    {"trait": "trait name (e.g. 'detail-oriented', 'externally-validated', 'risk-averse')",
     "confidence": "high | medium | low",
     "reason": "anchored to specific profile features"}
  ],
  "red_flags": ["specific concrete features that would warrant caution, with the reason"],
  "green_flags": ["specific concrete features that signal substance, with the reason"],
  "recommended_first_message_angle": "ONLY include this field if SPOTLIGHT FOCUS includes 'dating' — a specific opening angle calibrated to the profile, not a template",
  "recommended_business_approach": "ONLY include this field if SPOTLIGHT FOCUS includes 'workplace' or PLATFORM is 'linkedin' — how to open / pitch / reach out",
  "crisis_flag": false,
  "confidence_overall": "high | medium | low"
}

Rules:
- Profile reads are inherently lower confidence than message reads. Default 'medium' unless the profile is dense and specific.
- Cite features verbatim where possible ("the bio's third line:", "their second photo features...")
- Never moralize or fantasy-diagnose. Describe signals, never disorders.
- If the profile contains crisis content, set crisis_flag=true.
- Do NOT include the recommended_*_angle fields if the spotlight does not match.
"""


def build_analyze_profile_prompt(
    *,
    profile_content: str,
    platform: str,
    platform_prompt: str,
    spotlight_prompt: str,
    spotlight: str,
) -> str:
    parts: list[str] = [
        ANALYZE_PROFILE_INSTRUCTION,
        "",
        f"PLATFORM CONTEXT:\n{platform_prompt}",
        "",
        f"SPOTLIGHT FOCUS:\n{spotlight_prompt}",
        "",
        f"USER SPOTLIGHT (raw): {spotlight}",
        f"PROFILE PLATFORM (raw): {platform}",
        "",
        "---BEGIN PROFILE CONTENT---",
        profile_content.strip(),
        "---END PROFILE CONTENT---",
        "",
        "Return ONLY a single JSON object matching the schema above. No prose, no markdown.",
    ]
    return "\n".join(parts)
