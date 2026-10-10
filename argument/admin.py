from django.contrib import admin
from .models import Choice, ChoiceSession

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("round_number", "title", "round_type", "active")
    list_filter = ("round_number", "round_type", "active")
    search_fields = ("title", "label")

@admin.register(ChoiceSession)
class ChoiceSessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
