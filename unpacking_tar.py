from subprocess import call
from os import listdir, chdir
import platform

def unpacking_tar():
    #Solo se hara en la computadora que se ellame "u1"... funciona en ubuntu
    if platform.node() == "u1":
        list_number = []
        for i in listdir("./models/"):
            if i.find(".tar.gz") != -1:
                list_number.append(i[:8]+i[9:15])
        list_number = sorted(list_number)
        if len(list_number) >= 1:
            if len(listdir("models/train/")) > 0:
                call("rm -r models/train/*", shell=True)
            modelo = list_number[-1][:8] + "-" + list_number[-1][8:] + ".tar.gz"
            print("EL MODELO ES",modelo)
            call("ls", shell=True)
            call("mv models/{} models/train/.".format(modelo), shell=True)
            chdir('models/train')
            call(" tar -xzvf {}".format(modelo), shell=True)
            chdir("../")
            lista_2 = listdir(".")
            for i in lista_2:
                if i.find(".tar.gz") != -1:
                    call("rm "+i,shell=True)
            chdir('../')
        else:
            if len(listdir("./models/train/")) == 0:
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                print("SOLO EJECUTA \"rasa train\"")
                exit()