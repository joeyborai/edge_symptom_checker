from django.shortcuts import render
from datetime import date

from symptom_check.models import Athlete
# Create your views here.

def index(request):
    first_athlete = Athlete(first_name='Joseph', last_name='Favia')
    first_athlete.save()
    users = Athlete.objects.get(first_name="*")

    context = {
        'users': users,
        'day': str(date.today())
    }

    return render(request, 'symptom_form/index.html', context)

def add_user(request):
    print('Add')

def submit(request):
    users = ['Tom', 'Joe', 'Brett']

    context = {
        'users': users,
        'day': str(date.today())
    }

    return render(request, 'symptom_form/index.html', context)

