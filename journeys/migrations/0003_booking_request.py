from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("journeys", "0002_journey_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(editable=False, max_length=24, unique=True)),
                ("full_name", models.CharField(max_length=160)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=40)),
                ("country_of_residence", models.CharField(max_length=100)),
                ("travelers", models.PositiveSmallIntegerField(default=1)),
                ("adults", models.PositiveSmallIntegerField(default=1)),
                ("children", models.PositiveSmallIntegerField(default=0)),
                ("preferred_departure", models.CharField(blank=True, max_length=120)),
                ("departure_city", models.CharField(blank=True, max_length=120)),
                ("room_preference", models.CharField(blank=True, max_length=80)),
                ("passport_status", models.CharField(blank=True, max_length=80)),
                ("special_occasion", models.CharField(blank=True, max_length=160)),
                ("dietary_requirements", models.CharField(blank=True, max_length=240)),
                ("accessibility_requirements", models.CharField(blank=True, max_length=240)),
                ("emergency_contact_name", models.CharField(blank=True, max_length=160)),
                ("emergency_contact_phone", models.CharField(blank=True, max_length=40)),
                ("special_requests", models.TextField(blank=True)),
                ("budget_note", models.CharField(blank=True, max_length=160)),
                ("status", models.CharField(choices=[("new", "New"), ("reviewing", "Reviewing"), ("contacted", "Contacted"), ("confirmed", "Confirmed")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("journey", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="booking_requests", to="journeys.journey")),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
