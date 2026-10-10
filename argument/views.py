import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, ChoiceSession
from .services import calculate_profile, get_dna_rows, get_identity

FALLBACK_CHOICES = {
    1: [
        {
            "id": "wild",
            "label": "05:15 AM",
            "title": "WAKE UP TO THE WILD",
            "body": "The first light hits the savanna. Something moves beyond the tent.",
            "weight": {"adventure": 3, "nature": 3, "exploration": 2, "story": 1},
        },
        {
            "id": "curtains",
            "label": "08:30 AM",
            "title": "OPEN THE CURTAINS",
            "body": "Snow-covered mountains. Breakfast waiting. Nothing on the clock.",
            "weight": {"slow_travel": 3, "nature": 2, "luxury": 2, "story": 1},
        },
    ],
    2: [
        {
            "id": "kyoto",
            "label": "KYOTO / 20:40",
            "title": "A TABLE FOR TWO",
            "body": "A tiny counter. Seven seats. One chef. You have nowhere else to be.",
            "weight": {"culture": 3, "slow_travel": 2, "story": 2},
        },
        {
            "id": "kenya",
            "label": "KENYA / 21:10",
            "title": "UNDER A WIDE SKY",
            "body": "A campfire burns outside your tent. The night is louder than the silence.",
            "weight": {"adventure": 3, "nature": 3, "story": 2},
        },
    ],
    3: [
        {
            "id": "rail",
            "label": "THE LONG WAY",
            "title": "TAKE THE SCENIC ROUTE",
            "body": "A slower train. A window seat. The landscape becomes part of the story.",
            "weight": {"exploration": 3, "slow_travel": 3, "story": 2},
        },
        {
            "id": "city",
            "label": "RIGHT INTO IT",
            "title": "FOLLOW THE CITY LIGHTS",
            "body": "Arrive late. Walk farther. Find the neighbourhood everyone else missed.",
            "weight": {"culture": 3, "exploration": 3, "adventure": 2},
        },
    ],
}

def _choices_for_round(round_number):
    db_choices = list(
        Choice.objects.filter(round_number=round_number, active=True)
    )
    if db_choices:
        return [
            {
                "id": choice.pk,
                "label": choice.label,
                "title": choice.title,
                "body": choice.body,
                "weight": choice.profile_weights,
                "image_url": choice.image_url,
            }
            for choice in db_choices
        ]
    return FALLBACK_CHOICES.get(round_number, [])

def home(request):
    return render(request, "argument/home.html", {
        "choices": _choices_for_round(1),
    })

def argument_round(request, round_number):
    if round_number not in (2, 3):
        round_number = 2

    return render(request, "argument/round.html", {
        "round_number": round_number,
        "choices": _choices_for_round(round_number),
    })

@require_POST
def save_choice(request):
    payload = json.loads(request.body or "{}")
    selected = payload.get("choice")

    # Trust the database weights, not browser-supplied scoring data.
    db_choice = None
    try:
        db_choice = Choice.objects.get(pk=int(selected), active=True)
    except (TypeError, ValueError, Choice.DoesNotExist):
        pass

    weights = db_choice.profile_weights if db_choice else payload.get("weight", {})
    choices = request.session.get("travel_choices", [])
    choices.append({"choice": selected, "weight": weights})

    profile = calculate_profile(choices)
    request.session["travel_choices"] = choices
    request.session["travel_profile"] = profile
    request.session.modified = True
    request.session.save()

    # Persist the evolving Travel DNA as a real Django/PostgreSQL record.
    ChoiceSession.objects.update_or_create(
        session_key=request.session.session_key,
        defaults={"choices": choices, "profile": profile},
    )

    return JsonResponse({
        "success": True,
        "profile": profile,
        "choice_count": len(choices),
    })


def reveal(request):
    choices = request.session.get("travel_choices", [])

    # Never show fake/default DNA. The reveal belongs to the completed journey.
    if len(choices) < 3:
        return redirect("argument:home")

    profile = request.session.get("travel_profile") or calculate_profile(choices)
    return render(request, "argument/reveal.html", {
        "profile": profile,
        "dna_rows": get_dna_rows(profile),
        "identity": get_identity(profile),
        "choice_count": len(choices),
    })
