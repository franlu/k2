#-*- coding: utf-8 -*-
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from k2Ejercicio.models import Materia, Tema

@dajaxice_register
def updateMaterias(request, option):
    dajax = Dajax()
    options = Materia.objects.filter(curso=int(option))
    out = []
    out.append('<option value="" selected="selected">---------</option>')
    if options.count > 0:
        for option in options:
            out.append("<option value='%s'>%s</option>" % (option.id, option))
            print option

    dajax.assign('#id_materia', 'innerHTML', ''.join(out))
    return dajax.json()

@dajaxice_register
def updateTemas(request, option):
    dajax = Dajax()
    options = Tema.objects.filter(materia=int(option))
    out = []
    out.append('<option value="" selected="selected">---------</option>')
    if options.count > 0:
        for option in options:
            out.append("<option value='%s'>%s</option>" % (option.id, option))

    dajax.assign('#id_tema', 'innerHTML', ''.join(out))
    return dajax.json()