# -*- coding: utf-8 -*-
import floppyforms as forms

from k2Usuario.models import Alumno, Clase, Profesor

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        widgets = {
            'username': forms.TextInput,
            'password': forms.PasswordInput,
        }



class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        widgets = {
            'nombre': forms.TextInput,
        }