# -*- coding: utf-8 -*-

import django.contrib.auth as auth
import django.contrib.auth.views as authviews
import django.http as http

from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.generic import ListView

from k2Usuario.models import Alumno, Clase, Profesor
from k2Usuario.forms import AlumnoForm, ClaseForm

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
    context_object_name = 'clases'

class AlumnoList(ListView):
    model = Alumno
    context_object_name = 'alumnos'

class AlumnosClaseList(ListView):

    context_object_name = 'alumnos'
    template_name = 'k2Usuario/alumnos_clase_list.html'

    def get_queryset(self):
        self.clase = get_object_or_404(Clase, id=self.kwargs['clase_id'])
        return Alumno.objects.filter(clase=self.clase)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(AlumnosClaseList, self).get_context_data(**kwargs)
    # Add in the publisher
        context['clase'] = self.clase
        return context

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
