#! /usr/bin/python
import os

#buscamos el directorio en el que estamos konecta2scripts
directorioOriginal = os.getcwd()
print directorioOriginal

home=os.environ['HOME']
print home

f=open(home+"/.bashrc","a")
f.write("\nDIRECTORIO_SCRIPTS=\""+directorioOriginal+"\"")
f.write("\nalias cambiarpc=\'python "+directorioOriginal+"/cambiarPC.py\'")
f.close()