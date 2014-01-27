#! /usr/bin/python
import os

#buscamos el directorio en el que estamos konecta2scripts
#para que funcione desde cualquier sition
home=os.environ['HOME']
    
f=open(home+"/.bashrc")
archivo=f.read()
lugar=archivo.index("DIRECTORIO_SCRIPTS=")
f.seek(lugar+20)
direccion= f.readline()
  
directorioOriginal = direccion.partition("\"")[0]
print directorioOriginal
  
#buscamos la carpeta de konecta2
os.chdir(directorioOriginal)
os.chdir(os.pardir)
directorio = os.getcwd()
print directorio

def crear_pc():
     #nos hace falta el usuario del pc
    usuario=raw_input("Usuario:")
    #la contrasena de la base de datos de konecta2
    contrasena=raw_input("Contrasena base datos:")
    
    #abrimos el archivo de las configuraciones disponibles
    f=open(directorioOriginal+"/configuraciones/conf.disp","r")
    existe=False
    #mostramos todos los pc creados
    for linea in f:
        if linea == usuario+"\n":
            existe=True
    f.close()       
    print "<-------------0---------------->"
    
    if existe==False:
        #creamos una configuracion nueva con el nombre del pc
        os.system("cp "+directorioOriginal+"/configuraciones/config.py "+directorioOriginal+"/configuraciones/"
              +usuario+"_config.py")
        
        #y le anadimos lo correspondiente a dicho usuario
        f=open(directorioOriginal+"/configuraciones/"+usuario+"_config.py","a")
        f.write("#ruta del directorio principal de konecta2 \n"
            +"ruta_imagen_konecta2 = \""+directorio+"\"")
        f.write("\ncontrasena=\'"+contrasena+"\'")
        f.close()
        
        file(directorioOriginal+"/configuraciones/"+usuario+"_konecta2.wsgi","w")
        f=open(directorioOriginal+"/configuraciones/"+usuario+"_konecta2.wsgi","a")
        f.write("import os, sys\n"+
                "sys.path.append(\'"+home+"\')\n"+
                "sys.path.append(\'"+directorio+"\')\n"+
                "os.environ[\'DJANGO_SETTINGS_MODULE\']=\'konecta2.settings\'\n"+
                "import django.core.handlers.wsgi\n"+
                "application = django.core.handlers.wsgi.WSGIHandler()")
        f.close()
        
        #ademas anadimos el usuario al archivo de conf.disp
        f=open(directorioOriginal+"/configuraciones/conf.disp","a")
        f.flush()
        f.write(usuario+"\n")
        f.close
        print "Configuracion creada"
        
    else:
        print "Configuracion ya existe"
        
    
    

def cambiar_pc():
    
        f=open(directorioOriginal+"/configuraciones/conf.disp","r")
        n=0
        for linea in f:
            print n,"--->"+linea
            n=n+1
        
        seleccion=input("Seleccione el pc: ")
        m=0
        usuario=""
        f=open(directorioOriginal+"/configuraciones/conf.disp","r")
        for linea in f:
            if m==seleccion:
                usuario=linea
            m=m+1
        f.close()
        print "Comprobando usuario"
        usuario=usuario.partition("\n")[0] 
        print "Nuevo usuario: "+ usuario
        print "Borrando anterior configuracion"
        os.system("rm "+directorio+"/konecta2/config.py")
        os.system("rm "+directorio+"/konecta2.wsgi")
        print "Copiando nueva configuracion"
        os.system("cp "+directorioOriginal+"/configuraciones/"+usuario+"_config.py "+directorio+"/konecta2/config.py" ) 
        os.system("cp "+directorioOriginal+"/configuraciones/"+usuario+"_konecta2.wsgi "+directorio+"/konecta2.wsgi" ) 
        
        
def eliminar_pc():
        f=open(directorioOriginal+"/configuraciones/conf.disp","r")
        n=0
        for linea in f:
            print n,"--->"+linea
            n=n+1
        
        seleccion=input("Seleccione el pc: ")
        m=0
        usuario=""
        f=open(directorioOriginal+"/configuraciones/conf.disp","r")
        archivo=""
        f.seek(0)
        for linea in f:
            if m==seleccion:
                usuario=linea
            else:
                archivo=archivo+linea
            m=m+1
        
        f.close()
        usuario=usuario.partition("\n")[0]
        f=open(directorioOriginal+"/configuraciones/conf.disp","w")
        f.write(archivo)
        f.close()
        print "Comprobando usuario" 
        os.system("rm "+directorioOriginal+"/configuraciones/"+usuario+"_config.py ") 
        os.system("rm "+directorioOriginal+"/configuraciones/"+usuario+"_konecta2.wsgi ") 
        print "Pc eliminado"
        



#comienza el script

def menu():
    os.system("clear")
    print "<---Que desea hacer?---->"
    print "1.-Crear pc"
    print "2.-Cambiar pc"
    print "3.-Eliminar pc"
    print "4.-Salir"
    print "<----------------------->"
    
    opcion=raw_input("Elija una opcion:")
    #creamos el pc de un usuario
    if opcion=="1":
       crear_pc()
       raw_input("Pulse intro para continuar")
       menu()
    else: 
        #cambiamos de pc
        if opcion=="2":
            cambiar_pc()
            raw_input("Pulse intro para continuar")
            menu()
        else:   
            if opcion=="3":
                eliminar_pc()
                raw_input("Pulse intro para continuar")
                menu()
            else:   
                if opcion=="4":
                    print "Hasta Luego"
                else:
                    menu()
        

menu()