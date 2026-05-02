"""Per-platform attention vectors for /analyze/profile.

Each module exports PLATFORM_PROMPT — appended to the base profile prompt to
focus the model on what matters most on that surface (status signaling on
LinkedIn, ironic register on X, prompt-card structure on Hinge etc.).
"""
from app.prompts.profile_platforms import (
    bumble,
    generic,
    hinge,
    instagram,
    linkedin,
    reddit,
    tiktok,
    tinder,
    x,
)

PLATFORM_PROMPTS: dict[str, str] = {
    "linkedin": linkedin.PLATFORM_PROMPT,
    "x": x.PLATFORM_PROMPT,
    "instagram": instagram.PLATFORM_PROMPT,
    "tiktok": tiktok.PLATFORM_PROMPT,
    "reddit": reddit.PLATFORM_PROMPT,
    "hinge": hinge.PLATFORM_PROMPT,
    "bumble": bumble.PLATFORM_PROMPT,
    "tinder": tinder.PLATFORM_PROMPT,
    "generic": generic.PLATFORM_PROMPT,
}


def get_platform_prompt(platform: str) -> str:
    return PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["generic"])
