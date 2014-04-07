from django.contrib import admin
from k2Ejercicio.models import Ejercicio, Dificultad, TipoEjercicio, Tema, Materia, Curso, Contenido
from k2Ejercicio.models import EjercicioEnviado, EstadoEjercicios, Pregunta

admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(Tema)
admin.site.register(TipoEjercicio)
admin.site.register(Dificultad)
admin.site.register(Contenido)
admin.site.register(Ejercicio)
admin.site.register(EjercicioEnviado)
admin.site.register(EstadoEjercicios)
admin.site.register(Pregunta)

"""admin.site.register(Notificacion)
admin.site.register(Corregir)
admin.site.register(EjerciciosPendientes)
admin.site.register(Incidencias)
admin.site.register(Observaciones)
admin.site.register(EstadoEjercicios)
admin.site.register(EjerciciosAll)"""