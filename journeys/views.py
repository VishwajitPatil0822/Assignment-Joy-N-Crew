from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import BookingRequest, Journey


def _journey_context(journey):
    return {
        "journey": journey,
        "highlights": journey.highlights or [],
        "hotels": journey.hotels or [],
        "inclusions": journey.inclusions or [],
        "days": journey.days.all(),
        "experiences": journey.experiences.all(),
    }


def detail(request, slug):
    journeys = Journey.objects.filter(active=True).prefetch_related(
        "days", "experiences"
    )

    journey = next(
        (item for item in journeys if slugify(item.country) == slug or slugify(item.name) == slug),
        None,
    )

    if journey is None:
        raise Http404("Journey not found")

    return render(
        request,
        "journeys/detail.html",
        _journey_context(journey),
    )


def japan(request):
    return detail(request, "japan")


def book(request, slug):
    journeys = Journey.objects.filter(active=True)
    journey = next(
        (item for item in journeys if slugify(item.country) == slug or slugify(item.name) == slug),
        None,
    )
    if journey is None:
        raise Http404("Journey not found")

    if request.method == "POST":
        form_data = request.POST
        booking = BookingRequest.objects.create(
            journey=journey,
            full_name=form_data.get("full_name", "").strip(),
            email=form_data.get("email", "").strip(),
            phone=form_data.get("phone", "").strip(),
            country_of_residence=form_data.get("country_of_residence", "").strip(),
            travelers=int(form_data.get("travelers") or 1),
            adults=int(form_data.get("adults") or 1),
            children=int(form_data.get("children") or 0),
            preferred_departure=form_data.get("preferred_departure", "").strip(),
            departure_city=form_data.get("departure_city", "").strip(),
            room_preference=form_data.get("room_preference", "").strip(),
            passport_status=form_data.get("passport_status", "").strip(),
            special_occasion=form_data.get("special_occasion", "").strip(),
            dietary_requirements=form_data.get("dietary_requirements", "").strip(),
            accessibility_requirements=form_data.get("accessibility_requirements", "").strip(),
            emergency_contact_name=form_data.get("emergency_contact_name", "").strip(),
            emergency_contact_phone=form_data.get("emergency_contact_phone", "").strip(),
            special_requests=form_data.get("special_requests", "").strip(),
            budget_note=form_data.get("budget_note", "").strip(),
        )
        return render(
            request,
            "journeys/booking_success.html",
            {"journey": journey, "booking": booking},
        )

    return render(request, "journeys/booking.html", {"journey": journey})


def japan(request):
    return detail(request, "japan")
