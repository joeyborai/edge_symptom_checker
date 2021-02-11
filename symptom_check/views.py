import os
import mimetypes
import sys

from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.views.generic import View

from symptom_check.form_manager import *
from symptom_check.models import Athlete
# Create your views here.

class MainView(View):
    def get(self, request, *args, **kwargs):
        users = Athlete.objects.all()
        users = [(user.first_name + '_' + user.last_name, user.first_name + ' ' + user.last_name) for user in users]

        context = {
            'users': users,
            'day': str(date.today())
        }

        return render(request, 'symptom_form/index.html', context)

    def post(self, request, *args, **kwargs):
        users = Athlete.objects.all()
        users = [(user.first_name + '_' + user.last_name, user.first_name + ' ' + user.last_name) for user in users]

        arguments = request.POST
        create_report(arguments)
        
        context = {
            'users': users,
            'day': str(date.today())
        }

        return render(request, 'symptom_form/index.html', context)


def add_user(request):
    arguments = request.POST
    user = Athlete(first_name=arguments['first_name'], last_name=arguments['last_name'])
    user.save()

    users = Athlete.objects.all()
    users = [(user.first_name + '_' + user.last_name, user.first_name + ' ' + user.last_name) for user in users]

    context = {
        'users': users,
        'day': str(date.today())
    }

    return render(request, 'symptom_form/index.html', context)

def reports(request):
    files = os.listdir('/var/www/html/edge_check_in/symptom_check/edge_records/')

    dates = [entry[-15:-5] for entry in files]
    dates = list(set(dates))

    context = {
            'dates': dates
    }

    return render(request, 'symptom_form/reports.html', context)

def get_report(request):
    day = request.POST['date']
    files = os.listdir('/var/www/html/edge_check_in/symptom_check/edge_records/')

    for entry in files:
        if day in entry and 'daily_record' in entry:
            file_name = str(entry)
            break

    file_path = '/var/www/html/edge_check_in/symptom_check/edge_records/' + file_name
    f1 = open(file_path, 'rb')

    mime_type, _ = mimetypes.guess_type(file_path)

    response = HttpResponse(f1, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file_name

    return response

