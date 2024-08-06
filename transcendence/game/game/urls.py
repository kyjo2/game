# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("game/", include("games.urls")),
    path("admin/", admin.site.urls),
]