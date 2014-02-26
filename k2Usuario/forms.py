# -*- coding: utf-8 -*-
import floppyforms as forms

from k2Usuario.models import Alumno, Clase, Profesor

class ImageThumbnailFileInput(forms.ClearableFileInput):
    template_name = 'k2Usuario/image_thumbnail.html'

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields={
            #'avatar'
        }
        widgets = {
            'username': forms.TextInput,
            'password': forms.PasswordInput,
            'estado': forms.TextInput,
            'avatar': ImageThumbnailFileInput,
            'nacimiento': forms.DateTimeInput
        }



class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        widgets = {
            'nombre': forms.TextInput,
        }