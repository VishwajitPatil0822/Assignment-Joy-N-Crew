from django.db import migrations

def seed_choices(apps, schema_editor):
    Choice = apps.get_model("argument", "Choice")
    data = [
        (1, "05:15 AM", "WAKE UP TO THE WILD", "The first light hits the savanna. Something moves beyond the tent.", {"adventure":3,"nature":3,"exploration":2,"story":1}, "moment"),
        (1, "08:30 AM", "OPEN THE CURTAINS", "Snow-covered mountains. Breakfast waiting. Nothing on the clock.", {"slow_travel":3,"nature":2,"luxury":2,"story":1}, "moment"),
        (2, "KYOTO / 20:40", "A TABLE FOR TWO", "A tiny counter. Seven seats. One chef. You have nowhere else to be.", {"culture":3,"slow_travel":2,"story":2}, "evening"),
        (2, "KENYA / 21:10", "UNDER A WIDE SKY", "A campfire burns outside your tent. The night is louder than the silence.", {"adventure":3,"nature":3,"story":2}, "evening"),
        (3, "THE LONG WAY", "TAKE THE SCENIC ROUTE", "A slower train. A window seat. The landscape becomes part of the story.", {"exploration":3,"slow_travel":3,"story":2}, "pace"),
        (3, "RIGHT INTO IT", "FOLLOW THE CITY LIGHTS", "Arrive late. Walk farther. Find the neighbourhood everyone else missed.", {"culture":3,"exploration":3,"adventure":2}, "pace"),
    ]
    for round_number, label, title, body, weights, round_type in data:
        Choice.objects.create(
            round_number=round_number,
            label=label,
            title=title,
            body=body,
            profile_weights=weights,
            round_type=round_type,
            active=True,
        )

class Migration(migrations.Migration):
    dependencies = [("argument", "0001_initial")]
    operations = [migrations.RunPython(seed_choices, migrations.RunPython.noop)]
