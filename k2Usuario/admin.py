from django.contrib import admin

from k2Usuario.models import Alumno, Profesor, Clase


admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Clase)