
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .views import StatsView

urlpatterns = [
    path(route='',view=StatsView.as_view()),
]

