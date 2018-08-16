# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from logistica.models import Actividad
import datetime
from .calendar import getEventsByMonitor, getEventsByEspacio

def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'app/home.html')
    return redirect(reverse(login_user))


def principal(request):
    if request.user.is_authenticated:
        actividades = Actividad.objects.filter(horario__inicio__gt=datetime.datetime.now(),
                                               horario__inicio__day=datetime.datetime.now().day)
        context = {'actividades': actividades}
        return render(request, 'app/principal.html', context)
    else:
        redirect('/')


def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect(reverse(home))
        else:
            context['error_login'] = 'Nombre de usuario o contraseña no válido!'
            return render(request, 'app/login.html', context)
    return render(request, 'app/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse(home))


def monitor(request, nombreMonitor):
    context = {'events': getEventsByMonitor(nombreMonitor)
               }
    return render(request, 'app/monitor.html', context)

def espacio(request, nombreEspacio):
    context = {'events': getEventsByEspacio(nombreEspacio)
               }
    return render(request, 'app/espacio.html', context)