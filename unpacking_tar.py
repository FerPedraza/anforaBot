from subprocess import call
from os import listdir, chdir
import platform

def unpacking_tar():
    #Solo se hara en la computadora que se ellame "u1"... funciona en ubuntu
    print("PASE 7"*5)
    if platform.node() == "u1":
        print("PASE 9" * 5)
        list_number = []
        for i in listdir("./models/"):
            print("PASE 11" * 5)
            if i.find(".tar.gz") != -1:
                print("PASE 14" * 5)
                list_number.append(i[:8]+i[9:15])
        list_number = sorted(list_number)
        if len(list_number) >= 1:
            print("PASE 18" * 5)
            if len(listdir("models/train/")) > 0:
                print("PASE 20" * 5)
                call("rm -r models/train/*", shell=True)
            print("PASE 22" * 5)
            modelo = list_number[-1][:8] + "-" + list_number[-1][8:] + ".tar.gz"
            print("="*30)
            print("EL MODELO ES",modelo)
            print("PASE 24" * 5)
            call("ls", shell=True)
            print("cp models/{} models/train/.".format(modelo))
            call("mv models/{} models/train/.".format(modelo), shell=True)
            print("PASE 26" * 5)
            chdir('models/train')
            print("PASE 28" * 5)
            call(" tar -xzvf {}".format(modelo), shell=True)
            print("PASE 30" * 5)
            chdir("../")
            call("rm *tar.gz", shell=True)
            #if len(list_number) > 1:
            #    print("PASE 32" * 5)
            #    print("PASO 27" * 10)
            #    for i in range(1,len(list_number)):
            #        print("PASE 35" * 5)
            #        rm_model = list_number[i][:8] + "-" + list_number[i][8:] + ".tar.gz"
            #        #if modelo != rm_model:
            #        call("rm {}".format(rm_model), shell=True)
            chdir('../')
            print("PASE 30*"*10)
            #call("ls", shell=True)
            print("PASE 41"*10)
        else:
            if len(listdir("./models/train/")) == 0:
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                print("SOLO EJECUTA \"rasa train\"")
                exit()





