# -*- coding: utf-8 -*-

import django.contrib.auth as auth
import django.contrib.auth.views as authviews
import django.http as http

from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.generic import ListView

from k2Usuario.models import Alumno, Clase, Profesor
from k2Usuario.forms import AlumnoForm, ClaseForm

def accesoweb(request):

    """
        Acceso a la web para profesores
    """

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                if Profesor.objects.filter(idusuario=user).count() >0:

                    auth.login(request, user)
                    try:
                        return http.HttpResponseRedirect("/pizarra/")
                    except:

                        salida = auth.logout(request)
                        return authviews.login(request)
                else:

                    salida = auth.logout(request)
                    return http.HttpResponseRedirect("/")
            else:

                salida = auth.logout(request)
                return authviews.login(request)
        else:

            salida = auth.logout(request)
            return authviews.login(request)
    else:

        salida = auth.logout(request)
        return authviews.login(request)

@login_required
def logoutweb(request):

    """
        Cerrar sesión en la web para profesores
    """
    auth.logout(request)
    return render_to_response('registration/logout.html', context_instance=RequestContext(request))

@login_required
def setClase(request):

    if request.method == 'POST':
        data = request.POST
        form = ClaseForm(data)

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/')
    else:
        form = ClaseForm()

    return render(request, 'k2Usuario/nuevaclase.html', {
        'form': form,
    })



class ClaseList(ListView):
    model = Clase


@login_required
def getClases(request):

    cl = None
    if Clase.objects.all().count() > 0:
        cl = Clase.objects.all()

    return render(request, 'k2Usuario/clase_list.html', {
        'object_list': cl,
    })

@login_required
def setAlumno(request):

    data = None
    if request.method == 'POST':
        data = request
        us = UserCreationForm(data.POST, prefix='usuario')
        al = AlumnoForm(data.POST, data.FILES, prefix='alumno')

        if us.is_valid() and al.is_valid():
            usuario = us.save()
            alumno = al.save(commit=False)
            alumno.idusuario = usuario
            alumno.save()
            return http.HttpResponseRedirect(reverse('pizarra'))

    else:
        us = UserCreationForm(prefix='usuario')
        al = AlumnoForm(prefix='alumno')


    return render(request, 'k2Usuario/nuevoalumno.html', {
        'uf': us,
        'af': al,
    })

@login_required
def getAlumnos(request):

    al = None
    if Alumno.objects.all().count() > 0:
        al = Alumno.objects.all()

    return render(request, 'k2Usuario/alumnos.html', {
        'alumnos': al,
    })

@login_required
def getAlumnosClase(request,clase_id):

    al = Alumno.objects.filter(clase=clase_id) or None
    clase = Clase.objects.get(id=clase_id) or None
    return render(request, 'k2Usuario/alumnos.html', {
        'alumnos': al,
        'clase': clase,
    })