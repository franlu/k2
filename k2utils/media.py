# -*- coding: utf-8 -*-

from konecta2.settings import MEDIA_AUDIO, MEDIA_VIDEO, MEDIA_IMAGE, COLLEGE_ID

import os
import pafy # DOC http://np1.github.io/pafy/
import urllib2

def get_video(urlvideo,id):

    lpath = ''
    try:
        video = pafy.new(urlvideo)
        name = video.title.replace(" ", "_").replace("\t", "_")
        name = str(name).decode(encoding='utf-8',errors='strict')
        lname = "%s_%s_%s" % (COLLEGE_ID,id, name)
        lpath = MEDIA_VIDEO + lname
        streams = video.streams

        sbest = None
        for s in streams:
            if s.extension == 'mp4' and s.get_filesize() < 10485760:
                lpath = lpath + '.' + s.extension
                sbest = s
                break
            else:
                if s.extension == '3gp' and s.get_filesize() < 10485760:
                    lpath = lpath + '.' + s.extension
                    sbest = s
                    break

        if sbest is not None:
            sbest.download(filepath=lpath)
        else:
            mp4s = [ s for s in streams if s.extension == 'mp4']
            menor = mp4s[0]
            for s in mp4s:
                if s.get_filesize < menor:
                    menor = s
                    lpath = lpath + '.' + s.extension
            menor.download(filepath=lpath)
    except Exception,e:
        print "SIN VIDEO"
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
