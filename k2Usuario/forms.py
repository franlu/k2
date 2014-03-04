# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import ModelForm

import floppyforms as forms

from k2Usuario.models import Alumno, Clase, Profesor

class ImageThumbnailFileInput(forms.ClearableFileInput):
    template_name = 'k2Usuario/image_thumbnail.html'

class Alumno1Form(forms.ModelForm):
    class Meta:
        model = Alumno
        exclude = {'idusuario','estado'}
        widgets = {
            'nacimiento': forms.DateTimeInput
        }

class AlumnoForm(forms.ModelForm):
    username = forms.TextInput
    class Meta:
        model = Alumno
        fields={
            'nacimiento',

        }

        widgets = {

            'nacimiento': forms.DateTimeInput
        }



class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        """widgets = {
            'nombre': forms.TextInput,
        }"""