# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import ModelForm

import floppyforms as forms
from k2Usuario.models import Alumno, Clase, Profesor


class AlumnoForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Alumno
        exclude = {
            'idusuario',
            'estado'
        }
        widgets = {
            'nacimiento': forms.DateTimeInput
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        exclude = {
            'idusuario',
            'estado'
        }
        widgets = {
            'nacimiento': forms.DateTimeInput
        }

class ClaseForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    class Meta:
        model = Clase
        widgets = {
            'nombre': forms.TextInput,
        }