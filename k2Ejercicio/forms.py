#-*- coding: utf-8 -*-

import floppyforms as forms
from k2Ejercicio.models import Curso, Materia, Tema, Ejercicio, Contenido


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
        TIPO_CHOICES = {
            (1,"Público"),
            (0,"Privado"),
        }
        widgets = {
            'tipo': forms.Select(choices=TIPO_CHOICES)
        }

class EjercicioForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Ejercicio
        exclude = {
            'profesor',
            'favorito',
            'centro',
            'descripcion',
            'herramientas',
            'media',
            'pregunta',
        }


class ContenidoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Contenido
        exclude = {
            'fecha',
            'tipo',
            'path',
        }
        widgets = {
            'url': forms.URLField(),
            'archivo' : forms.FileField()
        }