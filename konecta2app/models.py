from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models.signals import post_save


import os

PROJECT_PATH = os.path.dirname("__file__")

class Permisos (models.Model):
    idusuario                   = models.ForeignKey(User)
    crear_usuario				= models.CharField(max_length=5)
    ver_todos_usuarios          = models.CharField(max_length=5)
    modificar_usuario			= models.CharField(max_length=5)
    eliminar_usuario			= models.CharField(max_length=5)
    ver_notas					= models.CharField(max_length=5)
    modificar_notas				= models.CharField(max_length=5)
    crear_ejercicio             = models.CharField(max_length=5)
    modificar_ejercicio         = models.CharField(max_length=5)
    eliminar_ejercicio          = models.CharField(max_length=5)
    def __unicode__(self):
        return self.idusuario

class Cursos(models.Model):
    idcurso						= models.AutoField(primary_key=True)
    nombre_curso				= models.CharField(max_length=50)
    def __unicode__(self):
        return self.nombre_curso



class Profesor(models.Model):
    nombre                      = models.CharField(max_length=20)
    apellido1                   = models.CharField(max_length=20)
    apellido2                   = models.CharField(max_length=20, null=True, blank=True)
    idusuario					= models.ForeignKey(User)
    curso						= models.ManyToManyField(Cursos)
    estado                      = models.CharField(max_length=20)
    urlimagen                   = models.CharField(max_length=200)
    nacimiento                  = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre   


class CursosEjercicios(models.Model):
    idcursos                    = models.AutoField(primary_key=True)
    nombre                      = models.CharField(max_length=200)
    favorito                    = models.ManyToManyField(User)
    def __unicode__(self):
        return self.nombre

class MateriasEjercicios(models.Model):
    idmateria                   = models.AutoField(primary_key=True)
    nombre                      = models.CharField(max_length=200)
    curso                       = models.ForeignKey(CursosEjercicios)
    favorito                    = models.ManyToManyField(User)
    def __unicode__(self):
        return self.nombre

class Tema(models.Model):
    idtema                      = models.AutoField(primary_key=True)
    nombre                      = models.CharField(max_length=200)
    materia                     = models.ForeignKey(MateriasEjercicios)
    tipo                        = models.CharField(max_length=200)
    favorito                    = models.ManyToManyField(User)
    def __unicode__(self):
        return self.nombre

class Dificultad(models.Model):
    iddificultad    = models.AutoField(primary_key=True)
    nombre          = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre

class Tokenregister(models.Model):
    tokenid     = models.AutoField(primary_key=True)
    token       = models.CharField(max_length=80)
    userid      = models.ForeignKey(User)
    date        = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tokenid

class Ejercicios(models.Model):
    idcentro                    = models.CharField(max_length=200)
    idprofesor                  = models.ForeignKey(User)
    idejercicio                 = models.AutoField(primary_key=True)
    titulo                      = models.CharField(max_length=500)
    imagen                      = models.CharField(max_length=500)
    descripcion                 = models.CharField(max_length=3000)
    materia                     = models.ForeignKey(MateriasEjercicios)
    curso                       = models.ForeignKey(CursosEjercicios)
    dificultad                  = models.ForeignKey(Dificultad)
    tema                        = models.ForeignKey(Tema)
    resultado                   = models.CharField(max_length=500, null=True, blank=True)
    calculadora                 = models.CharField(max_length=1)
    interfaz                    = models.CharField(max_length=200)
    consejo                     = models.CharField(max_length=200)
    estado                      = models.CharField(max_length=200)
    tipo                        = models.CharField(max_length=2)
    def __unicode__(self):
        return self.titulo

class Invitado(models.Model):
    nombre                      = models.CharField(max_length=20)
    idusuario                   = models.ForeignKey(User)
    curso                       = models.ManyToManyField(Cursos)
    estado                      = models.CharField(max_length=20)
    def __unicode__(self):
        return self.nombre


class Alumno(models.Model):
    nombre                      = models.CharField(max_length=20)
    apellido1                   = models.CharField(max_length=20)
    apellido2                   = models.CharField(max_length=20, null=True, blank=True)
    idusuario                   = models.ForeignKey(User)
    curso                       = models.ManyToManyField(Cursos)
    estado                      = models.CharField(max_length=20)
    urlimagen                   = models.CharField(max_length=200)
    nacimiento                  = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre
    
 
     
class Notificacion(models.Model):
    idnotificacion              = models.AutoField(primary_key=True)
    idusuario                   = models.ForeignKey(User)
    date                        = models.DateTimeField()
    tipo                        = models.CharField(max_length=200)
    mensaje                     = models.CharField(max_length=200)
    def __unicode__(self):
        return self.idusuario


class TiposEjercicios(models.Model):
    idtipo                      = models.AutoField(primary_key=True)
    nombre                      = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre


class EjerciciosClase(models.Model):
    idejercicioclase            = models.AutoField(primary_key=True)
    idejercicio                 = models.ForeignKey(Ejercicios)
    fecha                       = models.DateTimeField()
    idusuario                   = models.ForeignKey(User)
    idprofesor                  = models.ForeignKey(Profesor)
    idclase                     = models.ForeignKey(Cursos)
    imagen                      = models.CharField(max_length=500)
    nota                        = models.CharField(max_length=10, null=True, blank=True)
    booleano                    = models.CharField(max_length=10, null=True, blank=True)
    resultado                   = models.CharField(max_length=500)
    tiemporealizacion           = models.CharField(max_length=100)
    intentos                    = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idusuario

class Controles(models.Model):
    idcontroles                 = models.AutoField(primary_key=True)
    idejercicio                 = models.ForeignKey(Ejercicios)
    fecha                       = models.CharField(max_length=100)
    idusuario                   = models.ForeignKey(User)
    idprofesor                  = models.ForeignKey(Profesor)
    idclase                     = models.ForeignKey(Cursos)
    imagen                      = models.CharField(max_length=500)
    nota                        = models.CharField(max_length=10, null=True, blank=True)
    booleano                    = models.CharField(max_length=10, null=True, blank=True)
    resultado                   = models.CharField(max_length=500)
    tiemporealizacion           = models.CharField(max_length=100)
    intentos                    = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idusuario

class Examenes(models.Model):
    idejecamenes                = models.AutoField(primary_key=True)
    idejercicio                 = models.ForeignKey(Ejercicios)
    fecha                       = models.CharField(max_length=100)
    idusuario                   = models.ForeignKey(User)
    idprofesor                  = models.ForeignKey(Profesor)
    idclase                     = models.ForeignKey(Cursos)
    imagen                      = models.CharField(max_length=500)
    nota                        = models.CharField(max_length=10, null=True, blank=True)
    booleano                    = models.CharField(max_length=10, null=True, blank=True)
    resultado                   = models.CharField(max_length=500)
    tiemporealizacion           = models.CharField(max_length=100)
    intentos                    = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idusuario

class Globales(models.Model):
    idglobales                  = models.AutoField(primary_key=True)
    idejercicio                 = models.ForeignKey(Ejercicios)
    fecha                       = models.DateTimeField(max_length=100)
    idusuario                   = models.ForeignKey(User)
    idprofesor                  = models.ForeignKey(Profesor)
    idclase                     = models.ForeignKey(Cursos)
    imagen                      = models.CharField(max_length=500)
    nota                        = models.CharField(max_length=10, null=True, blank=True)
    booleano                    = models.CharField(max_length=10, null=True, blank=True)
    resultado                   = models.CharField(max_length=500)
    tiemporealizacion           = models.CharField(max_length=100)
    intentos                    = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idusuario
            
class Corregir(models.Model):
    idcorregir                  = models.AutoField(primary_key=True)
    idusuario                   = models.ForeignKey(User)
    idejercicio                 = models.ForeignKey(Ejercicios)
    materia                     = models.ForeignKey(MateriasEjercicios)
    resultado                   = models.CharField(max_length=500)
    urlimagen                   = models.CharField(max_length=500)
    estado                      = models.CharField(max_length=500)
    fecha                       = models.CharField(max_length=100)
    numerointentos              = models.CharField(max_length=100)
    numeroimagenes              = models.CharField(max_length=100)
    numeropreguntas             = models.CharField(max_length=100)
    fallos                      = models.CharField(max_length=100)
    nota                        = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idusuario
    
class EjerciciosPendientes(models.Model):
    idpendientes                = models.AutoField(primary_key=True)
    idprofesor                  = models.ForeignKey(Profesor)
    idejercicio                 = models.ForeignKey(Ejercicios)
    idalumno                    = models.ForeignKey(User)
    idcorregir                  = models.ForeignKey(Corregir)
    fecha                       = models.CharField(max_length=100)
    def __unicode__(self):
        return self.idpendientes
    
class Incidencias(models.Model):
    idusuario                   = models.ForeignKey(User)
    comentario                  = models.CharField(max_length=2000)
    def __unicode__(self):
        return self.idusuario

class Observaciones(models.Model):
    idusuario                   = models.ForeignKey(User)
    comentario                  = models.CharField(max_length=2000)
    def __unicode__(self):
        return self.idusuario
