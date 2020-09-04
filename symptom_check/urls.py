from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name="symptom_check"),
    path('submit', views.submit, name="symptom_submit")
]
