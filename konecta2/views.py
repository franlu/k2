# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.utils.functional import wraps
from django.template.context import RequestContext


import django.http as http


@login_required()
def inicio(request):

    return http.HttpResponseRedirect(reverse('pizarra'))


@login_required()
def pizarra(request):
    return render_to_response('pizarra.html',context_instance=RequestContext(request))
