#-*- coding: utf-8 -*-

import django.http as http

from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView,UpdateView, DeleteView, FormView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from k2Ejercicio.models import Curso, Materia, Tema, Ejercicio, Contenido, Pregunta
from k2Ejercicio.forms import CursoForm, MateriaForm, TemaForm, EjercicioForm, ContenidoForm, TextoForm, RespuestaTextoForm
from k2Usuario.models import Profesor

from konecta2.settings import MEDIA_VIDEO, MEDIA_IMAGE, MEDIA_AUDIO, COLLEGE_ID
from k2utils.media import get_video, get_audio, get_image

import os


class CursoCreate(FormView):

    template_name = 'k2Ejercicio/curso_create.html'
    form_class = CursoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/cursos/')

        return render(request, self.template_name, {'form': form})

class CursoUpdate(UpdateView):

    template_name = 'k2Ejercicio/curso_update.html'
    form_class = CursoForm

    def get_object(self, queryset=None):
        return get_object_or_404(Curso, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, instance=self.get_object())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, instance=self.get_object())
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/cursos/')

        return render(request, self.template_name, {'form': form,})

class CursoDelete(DeleteView):

    template_name = 'k2Ejercicio/curso_delete.html'

    def get(self, request, *args, **kwargs):
        curso = get_object_or_404(Curso, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'curso': curso})

    def post(self, request, *args, **kwargs):
        curso = get_object_or_404(Curso, pk=self.kwargs['pk'])
        curso.delete()
        return http.HttpResponseRedirect('/pizarra/cursos/')

class CursoList(ListView):

    context_object_name = 'cursos'

    def get_queryset(self):
        by_id = Curso.objects.all().order_by('id')
        return by_id


class MateriaCreate(FormView):

    template_name = 'k2Ejercicio/materia_create.html'
    form_class = MateriaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/materias/')

        return render(request, self.template_name, {'form': form})

class MateriaUpdate(UpdateView):

    template_name = 'k2Ejercicio/materia_update.html'
    form_class = MateriaForm

    def get_object(self, queryset=None):
        return get_object_or_404(Materia, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, instance=self.get_object())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, instance=self.get_object())
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/materias/')

        return render(request, self.template_name, {'form': form,})

class MateriaDelete(DeleteView):

    template_name = 'k2Ejercicio/materia_delete.html'

    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'materia': materia})

    def post(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, pk=self.kwargs['pk'])
        materia.delete()
        return http.HttpResponseRedirect('/pizarra/materias/')

class MateriaList(ListView):

    context_object_name = 'materias'

    def get_queryset(self):
        by_id = Materia.objects.all().order_by('id')
        return by_id

class TemaCreate(FormView):

    template_name = 'k2Ejercicio/tema_create.html'
    form_class = TemaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            if tema.tipo == '0':
                tema.tipo = request.user.id
            else:
                tema.tipo = '-1'
            tema.save()
            return http.HttpResponseRedirect(reverse('temalist'))

        return render(request, self.template_name, {'form': form})

class TemaUpdate(UpdateView):

    template_name = 'k2Ejercicio/tema_update.html'
    form_class = TemaForm

    def get_object(self, queryset=None):
        return get_object_or_404(Tema, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, instance=self.get_object())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, instance=self.get_object())
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect('/pizarra/temas/')

        return render(request, self.template_name, {'form': form,})

class TemaDelete(DeleteView):

    template_name = 'k2Ejercicio/tema_delete.html'

    def get(self, request, *args, **kwargs):
        tema = get_object_or_404(Tema, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'tema': tema})

    def post(self, request, *args, **kwargs):
        tema = get_object_or_404(Tema, pk=self.kwargs['pk'])
        tema.delete()
        return http.HttpResponseRedirect('/pizarra/temas/')

class TemaList(ListView):

    context_object_name = 'temas'

    def get_queryset(self):
        by_id = Tema.objects.all().order_by('id')
        return by_id


class EjercicioCreate(FormView):

    template_name = 'k2Ejercicio/ejercicio_create.html'
    form_class = EjercicioForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=False)
            ejercicio.profesor = get_object_or_404(Profesor, idusuario=request.user)
            ejercicio.save()
            return http.HttpResponseRedirect(reverse('ejerciciodetail', args=[ejercicio.id]))

        return render(request, self.template_name, {'form': form})

class EjercicioUpdate(UpdateView):

    template_name = 'k2Ejercicio/ejercicio_update.html'
    form_class = EjercicioForm

    def get_object(self, queryset=None):
        return get_object_or_404(Ejercicio, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, instance=self.get_object())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, instance=self.get_object())
        if form.is_valid():
            ejercicio = form.save(commit=False)
            ejercicio.profesor = get_object_or_404(Profesor, idusuario=request.user)
            ejercicio.save()
            return http.HttpResponseRedirect(reverse('ejerciciolist'))

        return render(request, self.template_name, {'form': form,})

class EjercicioDelete(DeleteView):

    template_name = 'k2Ejercicio/ejercicio_delete.html'

    def get(self, request, *args, **kwargs):
        ejercicio = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'ejercicio': ejercicio})

    def post(self, request, *args, **kwargs):
        ejercicio = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        ejercicio.delete()
        return http.HttpResponseRedirect(reverse('ejerciciolist'))

class EjercicioList(ListView):

    context_object_name = 'ejercicios'

    def get_queryset(self):
        by_id = Ejercicio.objects.all().order_by('-fecha')
        return by_id
    

class EjercicioDetailView(DetailView):

    model = Ejercicio
    context_object_name = 'e'

    def get_context_data(self, **kwargs):
        context = super(EjercicioDetailView, self).get_context_data(**kwargs)
        context['contenido'] = ContenidoForm
        return context


class videocreate(CreateView):

    template_name = 'k2Ejercicio/video_create.html'
    form_class = ContenidoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'e': ej,'contenido' : form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        lurl = ''
        if form.is_valid():
            if request.FILES:
                url = '%s_%s' %(COLLEGE_ID, self.kwargs['pk'])
                lurl = MEDIA_VIDEO + url
                destination = open(lurl, 'wb+')
                for chunk in request.FILES['archivo'].chunks():
                    destination.write(chunk)
                destination.close()
            else:
                url = form['url'].value()
                try:
                    lurl = get_video(url,self.kwargs['pk'])
                except Exception, e:
                    print e
            ej.media.create(tipo='VIDEO', path=lurl)
            xml = "<Video %s>%s</Video>" % (1,lurl)
            ej.descripcion = ej.descripcion + xml
            ej.save()
            return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(self.kwargs['pk'],)))

        return render(request, self.template_name, {'form': form})


def videodelete(request,pk, pk1):
    try:
        c = get_object_or_404(Contenido, pk=pk1)
        lpath = c.path
        xml = '<Video 1>%s</Video>' % c.path
        c.delete()
        e = get_object_or_404(Ejercicio, pk=pk)
        e.descripcion = e.descripcion.replace(xml,'')
        e.save()
        if os.path.exists(lpath):
            os.remove(lpath)
            print "BORRADO: %s" % lpath
        else:
            print "No existe el fichero: %s" % lpath
    except Exception, e:
        print e

    return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(pk,)))

class imagecreate(CreateView):

    template_name = 'k2Ejercicio/image_create.html'
    form_class = ContenidoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'e': ej,'contenido' : form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        lurl = ''
        if form.is_valid():
            if request.FILES:
                url = '%s_%s' % (COLLEGE_ID, self.kwargs['pk'])
                lurl = MEDIA_IMAGE + url
                destination = open(lurl, 'wb+')
                for chunk in request.FILES['archivo'].chunks():
                    destination.write(chunk)
                destination.close()
            else:
                url = form['url'].value()
                try:
                    lurl = get_image(url,self.kwargs['pk'])
                except Exception, e:
                    print e
            ej.media.create(tipo='IMAGE', path=lurl)
            xml = "<Image %s>%s</Image>" % (1,lurl)
            ej.descripcion = ej.descripcion + xml
            ej.save()
            return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(self.kwargs['pk'],)))

        return render(request, self.template_name, {'form': form})

def imagedelete(request,pk, pk1):
    try:
        c = get_object_or_404(Contenido, pk=pk1)
        lpath = c.path
        xml = '<Image 1>%s</Image>' % c.path
        c.delete()
        e = get_object_or_404(Ejercicio, pk=pk)
        e.descripcion = e.descripcion.replace(xml,'')
        e.save()
        if os.path.exists(lpath):
            os.remove(lpath)
            print "BORRADO: %s" % lpath
        else:
            print "No existe el fichero: %s" % lpath
    except Exception, e:
        print e

    return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(pk,)))


class textocreate(CreateView):

    template_name = 'k2Ejercicio/texto_create.html'
    form_class = TextoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'e': ej,'contenido' : form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        if form.is_valid():
            pregunta = form.save()
            ej.pregunta.add(pregunta)
            xml = "<Texto %s>%s</Texto>" % (1,pregunta.enunciado)
            ej.descripcion = ej.descripcion + xml
            ej.save()
            return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(self.kwargs['pk'],)))

        return render(request, self.template_name, {'form': form})

def textodelete(request,pk, pk1):
    try:
        p = get_object_or_404(Pregunta, pk=pk1)
        xml = '<Texto 1>%s</Texto>' % p.enunciado
        p.delete()
        e = get_object_or_404(Ejercicio, pk=pk)
        e.descripcion = e.descripcion.replace(xml,'')
        e.save()
    except Exception, e:
        print e

    return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(pk,)))

class respuestatextocreate(CreateView):

    template_name = 'k2Ejercicio/respuestatexto_create.html'
    form_class = RespuestaTextoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'e': ej,'contenido' : form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ej = get_object_or_404(Ejercicio, pk=self.kwargs['pk'])
        if form.is_valid():
            el = form.save(commit=False)
            el.tipo = 'RESPUESTATEXTO'
            el.save()
            ej.pregunta.add(el)
            xml = "<Texto %s>%s</Texto><RespuestaTexto 1>%s</RespuestaTexto>" % (1,el.enunciado,el.respuesta)
            ej.descripcion = ej.descripcion + xml
            ej.save()
            return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(self.kwargs['pk'],)))

        return render(request, self.template_name, {'form': form})

def respuestatextodelete(request,pk, pk1):
    try:
        p = get_object_or_404(Pregunta, pk=pk1)
        xml = "<Texto %s>%s</Texto><RespuestaTexto 1>%s</RespuestaTexto>" % (1,p.enunciado,p.respuesta)
        p.delete()
        e = get_object_or_404(Ejercicio, pk=pk)
        e.descripcion = e.descripcion.replace(xml,'')
        e.save()
    except Exception, e:
        print e

    return http.HttpResponseRedirect(reverse('ejerciciodetail', args=(pk,)))