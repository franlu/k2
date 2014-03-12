# -*- coding: utf-8 -*-

def comun(request):

    d = {
        'username': request.user.username,
    }

    return d
