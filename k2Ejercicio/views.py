#-*- coding: utf-8 -*-

import django.contrib.auth as auth
import django.contrib.auth.views as authviews
import django.http as http

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt

from annoying.functions import get_object_or_None
from k2Ejercicio.models import Curso, Materia, Tema, Ejercicio
from k2Ejercicio.forms import CursoForm, MateriaForm, TemaForm, EjercicioForm

import datetime
import json
import pytz
import random
import string

def setCurso(request):

    if request.method == 'POST':
        data = request.POST
        form = CursoForm(data)

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/')
    else:
        form = CursoForm()

    return render(request, 'k2Ejercicio/nuevocurso.html', {
        'form': form,
    })

def getCursos(request):

    cu = None
    if Curso.objects.all().count() > 0:
        cu = Curso.objects.all()

    return render(request, 'k2Ejercicio/cursos.html', {
        'cursos': cu,
    })

def setMateria(request):

    if request.method == 'POST':
        data = request.POST
        form = MateriaForm(data)

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/')
    else:
        form = MateriaForm()

    return render(request, 'k2Ejercicio/nuevamateria.html', {
        'form': form,
    })

def getMaterias(request):

    ma = None
    if Materia.objects.all().count() > 0:
        ma = Materia.objects.all()

    return render(request, 'k2Ejercicio/materias.html', {
        'materias': ma,
    })

def setTema(request):

    if request.method == 'POST':
        data = request.POST
        form = TemaForm(data)

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/')
    else:
        form = TemaForm()

    return render(request, 'k2Ejercicio/nuevotema.html', {
        'form': form,
    })

def getTemas(request):

    te = None
    if Tema.objects.all().count() > 0:
        te = Tema.objects.all()

    return render(request, 'k2Ejercicio/temas.html', {
        'temas': te,
    })

def setEjercicio(request):

    if request.method == 'POST':
        data = request
        form = EjercicioForm(data.POST, data.FILES)

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/')
    else:
        form = EjercicioForm()

    return render(request, 'k2Ejercicio/nuevoejercicio.html', {
        'form': form,
    })

def getEjercicios(request):

    ej = None
    if Ejercicio.objects.all().count() > 0:
        ej = Ejercicio.objects.all()

    return render(request, 'k2Ejercicio/ejercicios.html', {
        'ejercicios': ej,
    })
