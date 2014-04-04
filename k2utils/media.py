# -*- coding: utf-8 -*-

from konecta2.settings import MEDIA_AUDIO, MEDIA_VIDEO, MEDIA_IMAGE

import os
import pafy # DOC http://np1.github.io/pafy/
import urllib2

def get_video(urlvideo,id):

    lpath = ''
    try:
        video = pafy.new(urlvideo)
        name = video.title.replace(" ", "_").replace("\t", "_")
        lname = "%s_%s" % (id, name)
        lpath = MEDIA_VIDEO + lname
        best = video.getbest()
        lpath = lpath + '.' + best.extension
        best.download(filepath=lpath)
    except Exception,e:
        print e

    return lpath

def get_audio(urlaudio,id):

    lpath = ''
    try:
        audio = pafy.new(urlaudio)
        name = audio.title.replace(" ", "_").replace("\t", "_")
        lname = "%s_%s" % (id, name)
        lpath = MEDIA_AUDIO + lname
        best = audio.getbestaudio()
        lpath = lpath + '.' + best.extension
        best.download(filepath=lpath)
    except Exception,e:
        print e

    return lpath

def get_image(urlimg,id):

    lname = "%s_%s" % (id, urlimg.split('/')[-1])
    lpath = MEDIA_IMAGE + lname

    if os.path.exists(lpath):
        os.remove(lpath)

    try:
        url = urllib2.build_opener()
        img1 = url.open(urlimg)
        limg = img1.read()
        fiout = open(lpath, "wb")
        fiout.write(limg)
        fiout.close()
    except Exception, e:
        print e

    return lpath
