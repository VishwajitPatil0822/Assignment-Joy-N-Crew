from collections import defaultdict

PROFILE_KEYS = (
    "story",
    "adventure",
    "nature",
    "culture",
    "exploration",
    "slow_travel",
    "luxury",
)

PROFILE_LABELS = {
    "story": "STORY",
    "adventure": "ADVENTURE",
    "nature": "NATURE",
    "culture": "CULTURE",
    "exploration": "EXPLORATION",
    "slow_travel": "SLOW TRAVEL",
    "luxury": "LUXURY",
}


def calculate_profile(selected_choices):
    """
    Infer Travel DNA from the user's actual choices.

    Each of the 3 rounds contributes equally. A trait can receive up to
    3 evidence points per round, so the theoretical maximum is 9 points.
    We deliberately map that evidence into a realistic 35–90 affinity band
    instead of pretending a person can be "100% story" after three clicks.

    This keeps the score comparable across users and prevents the strongest
    trait from automatically becoming 100 just because it is the largest.
    """
    scores = defaultdict(int)
    completed_rounds = min(len(selected_choices), 3)

    for choice in selected_choices[:3]:
        for key, value in choice.get("weight", {}).items():
            if key in PROFILE_KEYS:
                scores[key] += max(0, min(int(value), 3))

    if completed_rounds == 0:
        return {key: 0 for key in PROFILE_KEYS}

    theoretical_max = completed_rounds * 3

    profile = {}
    for key in PROFILE_KEYS:
        evidence = min(scores.get(key, 0), theoretical_max)
        evidence_ratio = evidence / theoretical_max

        # 35 = neutral baseline, 90 = strongest plausible affinity.
        profile[key] = round(35 + (55 * evidence_ratio))

    return profile


def get_dna_rows(profile, limit=4):
    """Return the strongest traits first for the reveal UI."""
    ranked = sorted(
        PROFILE_KEYS,
        key=lambda key: profile.get(key, 0),
        reverse=True,
    )
    return [
        {
            "key": key,
            "label": PROFILE_LABELS[key],
            "score": profile.get(key, 0),
            "display_score": f"{profile.get(key, 0) / 10:.1f}",
        }
        for key in ranked[:limit]
        if profile.get(key, 0) > 0
    ]


def get_identity(profile):
    if profile.get("story", 0) >= 80 or profile.get("exploration", 0) >= 80:
        return {
            "name": "THE STORY SEEKER",
            "copy": "You don't collect destinations. You collect stories.",
        }

    if profile.get("nature", 0) >= 75:
        return {
            "name": "THE WILD AT HEART",
            "copy": "You travel for the places that still feel untamed.",
        }

    return {
        "name": "THE CURIOUS DRIFTER",
        "copy": "You want a journey with enough room for surprise.",
    }
