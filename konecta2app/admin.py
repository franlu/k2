# -*- coding: utf-8 -*-
from django.contrib import admin
import konecta2app.models

admin.site.register(konecta2app.models.Cursos)
admin.site.register(konecta2app.models.MateriasEjercicios)
admin.site.register(konecta2app.models.CursosEjercicios)
admin.site.register(konecta2app.models.Permisos)
admin.site.register(konecta2app.models.Profesor)
admin.site.register(konecta2app.models.Alumno)
admin.site.register(konecta2app.models.Invitado)
admin.site.register(konecta2app.models.Dificultad)
admin.site.register(konecta2app.models.Tema)
admin.site.register(konecta2app.models.TiposEjercicios)
admin.site.register(konecta2app.models.Ejercicios)
#admin.site.register(konecta2app.models.Examenes)
admin.site.register(konecta2app.models.Notificacion)
admin.site.register(konecta2app.models.Corregir)
admin.site.register(konecta2app.models.EjerciciosPendientes)
admin.site.register(konecta2app.models.Incidencias)
admin.site.register(konecta2app.models.Observaciones)
admin.site.register(konecta2app.models.EstadoEjercicios)
admin.site.register(konecta2app.models.EjerciciosAll)