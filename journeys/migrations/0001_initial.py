from django.db import migrations, models
import django.db.models.deletion

def seed_japan(apps, schema_editor):
    Journey = apps.get_model("journeys", "Journey")
    JourneyDay = apps.get_model("journeys", "JourneyDay")
    Experience = apps.get_model("journeys", "Experience")

    journey = Journey.objects.create(
        name="Autumn Japan, Your Way",
        subtitle="A seasonal journey through Japan",
        country="Japan",
        route="TOKYO → OSAKA → TOKYO",
        duration="09 DAYS / 08 NIGHTS",
        starting_price=360000,
        departure="15 NOV 2026 · EX-MUMBAI",
        description="Nine days through Japan in autumn — city energy, seasonal colour and an excursion into Nikko.",
        why_match="You chose movement over routine. You chose stories over checklists. Japan gives you both.",
        profile_weights={"story": 92, "exploration": 86, "nature": 78, "slow_travel": 64},
        active=True,
    )

    experiences = [
        ("NIKKO AUTUMN", "Autumn excursion into Nikko."),
        ("JAPAN BY RAIL", "Experience Japan's rail network."),
        ("OSAKA", "Four nights based around Osaka."),
        ("TOKYO", "Begin and close the journey in Tokyo."),
    ]
    for title, description in experiences:
        Experience.objects.create(journey=journey, title=title, description=description)

    days = [
        (1, "TOKYO / ARRIVAL", "Arrive in Tokyo and settle into the rhythm of the city."),
        (2, "TOKYO / CITY & CONTRAST", "Explore Tokyo’s contrast of tradition, neighbourhoods and modern energy."),
        (3, "NIKKO / AUTUMN", "Follow the autumn trail into Nikko."),
        (4, "OSAKA / THE LONG STAY", "Four nights based around Osaka and its surrounding highlights."),
        (5, "OSAKA / THE LONG STAY", "Continue discovering Osaka at your own pace."),
        (6, "OSAKA / THE LONG STAY", "A day for the city’s neighbourhoods and food."),
        (7, "OSAKA / THE LONG STAY", "Your final full day around Osaka."),
        (8, "TOKYO / RETURN", "Return to Tokyo and close the journey with room for your own discoveries."),
        (9, "TOKYO / DEPARTURE", "Close the journey and depart."),
    ]
    for number, title, description in days:
        JourneyDay.objects.create(
            journey=journey,
            day_number=number,
            title=title,
            description=description,
        )

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Journey",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("subtitle", models.CharField(blank=True, max_length=220)),
                ("country", models.CharField(max_length=100)),
                ("route", models.CharField(max_length=220)),
                ("duration", models.CharField(max_length=60)),
                ("starting_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("departure", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField()),
                ("why_match", models.TextField(blank=True)),
                ("hero_image_url", models.URLField(blank=True)),
                ("profile_weights", models.JSONField(default=dict)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("country", "name")},
        ),
        migrations.CreateModel(
            name="JourneyDay",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("day_number", models.PositiveSmallIntegerField()),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("journey", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="days", to="journeys.journey")),
            ],
            options={"ordering": ("day_number",)},
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("journey", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="experiences", to="journeys.journey")),
            ],
        ),
        migrations.RunPython(seed_japan, migrations.RunPython.noop),
    ]
