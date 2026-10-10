from django.urls import path
from . import views

app_name = "journeys"

urlpatterns = [
    path("<slug:slug>/book/", views.book, name="book"),
    path("<slug:slug>/", views.detail, name="detail"),
]
