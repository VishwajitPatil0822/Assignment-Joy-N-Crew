from django.db import models

class Journey(models.Model):
    name = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=220, blank=True)
    country = models.CharField(max_length=100)
    route = models.CharField(max_length=220)
    duration = models.CharField(max_length=60)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    departure = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    why_match = models.TextField(blank=True)
    hero_image_url = models.URLField(blank=True)
    profile_weights = models.JSONField(default=dict)
    highlights = models.JSONField(default=list)
    hotels = models.JSONField(default=list)
    inclusions = models.JSONField(default=list)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("country", "name")

    def __str__(self):
        return self.name

class JourneyDay(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="days")
    day_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=180)
    description = models.TextField()

    class Meta:
        ordering = ("day_number",)

    def __str__(self):
        return f"{self.journey.name} — Day {self.day_number}"

class Experience(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("contacted", "Contacted"),
        ("confirmed", "Confirmed"),
    ]

    journey = models.ForeignKey(Journey, on_delete=models.PROTECT, related_name="booking_requests")
    reference = models.CharField(max_length=24, unique=True, editable=False)
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    country_of_residence = models.CharField(max_length=100)
    travelers = models.PositiveSmallIntegerField(default=1)
    adults = models.PositiveSmallIntegerField(default=1)
    children = models.PositiveSmallIntegerField(default=0)
    preferred_departure = models.CharField(max_length=120, blank=True)
    departure_city = models.CharField(max_length=120, blank=True)
    room_preference = models.CharField(max_length=80, blank=True)
    passport_status = models.CharField(max_length=80, blank=True)
    special_occasion = models.CharField(max_length=160, blank=True)
    dietary_requirements = models.CharField(max_length=240, blank=True)
    accessibility_requirements = models.CharField(max_length=240, blank=True)
    emergency_contact_name = models.CharField(max_length=160, blank=True)
    emergency_contact_phone = models.CharField(max_length=40, blank=True)
    special_requests = models.TextField(blank=True)
    budget_note = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.reference:
            import uuid
            self.reference = f"JNC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} — {self.full_name}"
