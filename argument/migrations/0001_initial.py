from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Choice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("round_number", models.PositiveSmallIntegerField()),
                ("label", models.CharField(max_length=160)),
                ("title", models.CharField(max_length=180)),
                ("body", models.TextField()),
                ("image_url", models.URLField(blank=True)),
                ("profile_weights", models.JSONField(default=dict)),
                ("round_type", models.CharField(choices=[("moment", "Moment"), ("evening", "Evening"), ("pace", "Pace")], default="moment", max_length=20)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("round_number", "id")},
        ),
        migrations.CreateModel(
            name="ChoiceSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=64, unique=True)),
                ("choices", models.JSONField(default=list)),
                ("profile", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
