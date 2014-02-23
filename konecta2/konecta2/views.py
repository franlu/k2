# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils.functional import wraps
from django.template.context import RequestContext
import django.contrib.auth as auth
import django.contrib.auth.views as authviews

import django.http as http


def acceso(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        print "entra0"
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                try:
                    request.user.get_profile().set_session_key(request.session.session_key)
                    return http.HttpResponseRedirect("/pizarra/")
                except:
                    print "entra1"
                    salida = auth.logout(request)
                    return authviews.login(request)
            else:
                print "entra2"
                salida = auth.logout(request)
                return authviews.login(request)
        else:
            print "entra3"
            salida = auth.logout(request)
            return authviews.login(request)
    else:
        print "entra4"
        salida = auth.logout(request)
        return authviews.login(request)

def logout(request):
    auth.logout(request)
    return render_to_response('registration/logout.html', context_instance=RequestContext(request))


def pizarra(request):

    return render_to_response('pizarra.html',context_instance=RequestContext(request))