#-*- coding: utf-8 -*-

import floppyforms as forms
from k2Ejercicio.models import Curso, Materia, Tema, Ejercicio, Contenido, Pregunta

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class CursoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Curso
        exclude = {
            'favorito',
        }

class MateriaForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Materia
        exclude = {
            'favorito',
        }

class TemaForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Tema
        exclude = {
            'favorito',
        }

class EjercicioForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    calculadora = forms.CheckboxInput()
    tiempo = forms.CheckboxInput()
    class Meta:
        model = Ejercicio
        widgets = {
            'calculadora' : forms.CheckboxInput() ,
            'tiempo' : forms.CheckboxInput() ,
        }
        exclude = {
            'profesor',
            'favorito',
            'centro',
            'descripcion',
            'herramientas',
            'media',
            'pregunta',
        }


class ContenidoForm(forms.Form):
    error_css_class = 'alert alert-danger'

    url = forms.URLField(required=False)
    archivo = forms.FileField(required=False)

    class Meta:
        widgets = {
            'url': forms.URLField(),
            'archivo' : forms.ClearableFileInput()
        }

class TextoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'

    class Meta:
        model = Pregunta
        exclude = {
            'respuesta',
            'consejo',
            'nota_maxima',
            'tipo',
        }
        widgets = {
            'enunciado': forms.Textarea(attrs={'maxlength':2000, 'cols':200, 'rows':10,}),
        }

class RespuestaTextoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'

    class Meta:
        model = Pregunta
        exclude = {
            'nota_maxima',
            'tipo',
        }

