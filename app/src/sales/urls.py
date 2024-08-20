from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .views import SimpleView,TopProductsView,TopClientsView

urlpatterns = [
    path(route='',view=SimpleView.as_view()),
    path(route='products',view=TopProductsView.as_view()),
    path(route='clients',view=TopClientsView.as_view()),
]

