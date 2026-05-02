"""Spotlights — 8 onboarding focus areas. Each exports a SPOTLIGHT_PROMPT string."""
from app.prompts.spotlights import (
    conflict,
    dating,
    family,
    friendship,
    patterns,
    public_figure,
    self,
    workplace,
)

SPOTLIGHTS: dict[str, str] = {
    "dating": dating.SPOTLIGHT_PROMPT,
    "workplace": workplace.SPOTLIGHT_PROMPT,
    "family": family.SPOTLIGHT_PROMPT,
    "self": self.SPOTLIGHT_PROMPT,
    "friendship": friendship.SPOTLIGHT_PROMPT,
    "conflict": conflict.SPOTLIGHT_PROMPT,
    "public_figure": public_figure.SPOTLIGHT_PROMPT,
    "patterns": patterns.SPOTLIGHT_PROMPT,
}


def get_spotlight_prompt(spotlight: str) -> str:
    return SPOTLIGHTS.get(spotlight, SPOTLIGHTS["self"])
