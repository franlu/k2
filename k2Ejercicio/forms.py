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
        }


class ContenidoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Contenido
        exclude = {
            'texto',
        }