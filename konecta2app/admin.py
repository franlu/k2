from django.contrib import admin
from konecta2app.models import TiposEjercicios, Permisos, Dificultad, Tema, MateriasEjercicios, CursosEjercicios, Cursos, Profesor, Alumno, Invitado, Ejercicios

admin.site.register(Cursos)
admin.site.register(MateriasEjercicios)
admin.site.register(CursosEjercicios)
admin.site.register(Permisos)
admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Invitado)
admin.site.register(Dificultad)
admin.site.register(Tema)
admin.site.register(TiposEjercicios)
admin.site.register(Ejercicios)
