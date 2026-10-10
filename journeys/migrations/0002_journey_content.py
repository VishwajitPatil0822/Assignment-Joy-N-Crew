from django.db import migrations, models


def seed_content(apps, schema_editor):
    Journey = apps.get_model("journeys", "Journey")
    JourneyDay = apps.get_model("journeys", "JourneyDay")
    Experience = apps.get_model("journeys", "Experience")

    japan = Journey.objects.filter(country__iexact="Japan").first()
    if japan:
        japan.highlights = [
            "Autumn colour in Nikko",
            "Tokyo's old-meets-new neighbourhoods",
            "Shinkansen journey through Japan",
            "Four-night Osaka base",
            "A final Tokyo return for your own discoveries",
        ]
        japan.hotels = [
            {"city": "TOKYO", "nights": "3 NIGHTS", "type": "Curated city hotel"},
            {"city": "OSAKA", "nights": "4 NIGHTS", "type": "Curated city hotel"},
            {"city": "TOKYO", "nights": "1 NIGHT", "type": "Airport-convenient stay"},
        ]
        japan.inclusions = [
            "8 nights accommodation",
            "Daily breakfast",
            "Selected intercity rail journeys",
            "Nikko autumn excursion",
            "Airport / intercity transfers as specified",
            "Joy-N-Crew trip coordination",
        ]
        japan.hero_image_url = "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=2200&q=85"
        japan.save()

    journeys = [
        {
            "name": "The Long Way South",
            "subtitle": "Wild coastlines, wide skies and room to wander",
            "country": "New Zealand",
            "route": "AUCKLAND → QUEENSTOWN → MILFORD SOUND → CHRISTCHURCH",
            "duration": "11 DAYS / 10 NIGHTS",
            "starting_price": 285000,
            "departure": "SELECTED SEASON · EX-MUMBAI",
            "description": "A slower road through New Zealand's landscapes — built for travellers who want the journey between places to matter.",
            "why_match": "You chose the scenic route. New Zealand rewards the people who leave space between the highlights.",
            "hero_image_url": "https://images.unsplash.com/photo-1469521669194-babb45599def?auto=format&fit=crop&w=2200&q=85",
            "profile_weights": {"exploration": 88, "nature": 92, "slow_travel": 86, "adventure": 78},
            "highlights": ["Southern Alps", "Milford Sound", "Scenic road journeys", "Queenstown", "Wild coastlines"],
            "hotels": [
                {"city": "AUCKLAND", "nights": "2 NIGHTS", "type": "Curated city hotel"},
                {"city": "QUEENSTOWN", "nights": "4 NIGHTS", "type": "Lakeside stay"},
                {"city": "CHRISTCHURCH", "nights": "2 NIGHTS", "type": "Design-led city hotel"},
            ],
            "inclusions": ["10 nights accommodation", "Daily breakfast", "Selected scenic transfers", "Milford Sound experience", "Trip coordination"],
            "days": [
                (1, "AUCKLAND / ARRIVAL", "Arrive, settle in and let the pace of the city introduce the journey."),
                (2, "AUCKLAND / THE EDGE", "A day of harbour views, neighbourhoods and the first taste of New Zealand."),
                (3, "QUEENSTOWN / SOUTH", "Fly south and trade the city skyline for mountains."),
                (4, "QUEENSTOWN / WILD", "A full day to choose between lake, trail and adrenaline."),
                (5, "MILFORD SOUND / THE LONG WAY", "Follow the road through landscapes that make the drive part of the destination."),
                (6, "QUEENSTOWN / SLOW DAY", "Leave the schedule open. This is where the journey breathes."),
                (7, "QUEENSTOWN / BEYOND", "Explore a quieter side of the region."),
                (8, "CHRISTCHURCH / NORTH", "Travel onward and watch the landscape change."),
                (9, "CHRISTCHURCH / CITY & COAST", "A day between heritage, food and the Pacific."),
                (10, "CHRISTCHURCH / LAST LIGHT", "Your final full day. Keep it yours."),
                (11, "DEPARTURE", "Close the journey and carry the long way home with you."),
            ],
        },
        {
            "name": "A Serenade of Savanna",
            "subtitle": "Wild nights, open skies and stories worth telling",
            "country": "Kenya",
            "route": "NAIROBI → AMBOSELI → MASAI MARA → NAIROBI",
            "duration": "08 DAYS / 07 NIGHTS",
            "starting_price": 320000,
            "departure": "SELECTED SEASON · EX-MUMBAI",
            "description": "A focused safari journey where the wild is not a backdrop — it is the reason you wake before sunrise.",
            "why_match": "You chose the wild when the world went quiet. Kenya turns that instinct into the journey.",
            "hero_image_url": "https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=2200&q=85",
            "profile_weights": {"adventure": 94, "nature": 96, "story": 82, "exploration": 86},
            "highlights": ["Amboseli sunrise", "Masai Mara game drives", "Campfire evenings", "Mount Kilimanjaro views", "Local cultural encounters"],
            "hotels": [
                {"city": "NAIROBI", "nights": "1 NIGHT", "type": "Boutique city stay"},
                {"city": "AMBOSELI", "nights": "2 NIGHTS", "type": "Safari camp"},
                {"city": "MASAI MARA", "nights": "4 NIGHTS", "type": "Tented safari camp"},
            ],
            "inclusions": ["7 nights accommodation", "Full-board safari stays", "Game drives", "Park fees", "Safari vehicle and guide", "Selected transfers"],
            "days": [
                (1, "NAIROBI / ARRIVAL", "Arrive in Kenya and ease into the rhythm before the wild begins."),
                (2, "AMBOSELI / FIRST LIGHT", "Head south. Wake to a landscape framed by Kilimanjaro."),
                (3, "AMBOSELI / WILD", "Sunrise game drive, long grasslands and a slower afternoon."),
                (4, "MASAI MARA / THE CROSSING", "Travel west into the Mara and let the landscape change around you."),
                (5, "MASAI MARA / DAWN", "A full day in the reserve, following the rhythm of the animals."),
                (6, "MASAI MARA / AFTER DARK", "Another day in the wild, ending around the campfire."),
                (7, "MASAI MARA / LAST SAFARI", "One final morning to follow whatever the landscape gives you."),
                (8, "NAIROBI / DEPARTURE", "Return to Nairobi and depart with a very different idea of silence."),
            ],
        },
    ]

    for data in journeys:
        if Journey.objects.filter(country=data["country"], active=True).exists():
            continue
        journey = Journey.objects.create(
            name=data["name"],
            subtitle=data["subtitle"],
            country=data["country"],
            route=data["route"],
            duration=data["duration"],
            starting_price=data["starting_price"],
            departure=data["departure"],
            description=data["description"],
            why_match=data["why_match"],
            hero_image_url=data["hero_image_url"],
            profile_weights=data["profile_weights"],
            highlights=data["highlights"],
            hotels=data["hotels"],
            inclusions=data["inclusions"],
            active=True,
        )
        for number, title, description in data["days"]:
            JourneyDay.objects.create(
                journey=journey,
                day_number=number,
                title=title,
                description=description,
            )
        for title in data["highlights"]:
            Experience.objects.create(
                journey=journey,
                title=title,
                description="A signature moment from this journey.",
            )


class Migration(migrations.Migration):
    dependencies = [
        ("journeys", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="journey",
            name="highlights",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="journey",
            name="hotels",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="journey",
            name="inclusions",
            field=models.JSONField(default=list),
        ),
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
