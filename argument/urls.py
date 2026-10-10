from django.urls import path
from . import views

app_name = "argument"

urlpatterns = [
    path("", views.home, name="home"),
    path("argument/<int:round_number>/", views.argument_round, name="round"),
    path("reveal/", views.reveal, name="reveal"),
    path("api/save-choice/", views.save_choice, name="save_choice"),
]
