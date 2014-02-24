# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils.functional import wraps
from django.template.context import RequestContext


def pizarra(request):

    return render_to_response('pizarra.html',context_instance=RequestContext(request))