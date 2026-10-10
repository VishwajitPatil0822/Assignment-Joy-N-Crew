from django.contrib import admin
from .models import BookingRequest, Experience, Journey, JourneyDay

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("country", "name", "duration", "starting_price", "active")
    list_filter = ("active", "country")
    search_fields = ("name", "country")

@admin.register(JourneyDay)
class JourneyDayAdmin(admin.ModelAdmin):
    list_display = ("journey", "day_number", "title")
    list_filter = ("journey",)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("journey", "title")
    list_filter = ("journey",)

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("reference", "journey", "full_name", "travelers", "status", "created_at")
    list_filter = ("status", "journey", "created_at")
    search_fields = ("reference", "full_name", "email", "phone")
    readonly_fields = ("reference", "created_at")
