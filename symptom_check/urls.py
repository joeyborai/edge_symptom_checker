from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name="symptom_check"),
    path('add_user', views.add_user, name="add_user"),
    path('get_report', views.get_report, name="get_report"),
    path('reports', views.reports, name="reports")
]
