from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("argument.urls")),
    path("journeys/", include("journeys.urls")),
]
