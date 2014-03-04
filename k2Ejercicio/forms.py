#-*- coding: utf-8 -*-

import floppyforms as forms
from k2Ejercicio.models import Curso, Materia, Tema, Ejercicio


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        exclude = {
            'favorito',
        }
        widgets = {
            'nombre': forms.TextInput
        }

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        exclude = {
            'favorito',
        }

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        exclude = {
            'favorito',
        }

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        exclude = {
            'favorito',
        }