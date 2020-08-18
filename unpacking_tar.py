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
            modelo = list_number[0][:8] + "-" + list_number[0][8:] + ".tar.gz"
            call("cp modelo /train/.")
            chdir('models')
            call(" tar -xzvf {}".format(modelo), shell=True)
            if len(list_number) > 1:
                print("PASO 27" * 10)
                for i in range(1,len(list_number)):
                    rm_model = list_number[i][:8] + "-" + list_number[i][8:] + ".tar.gz"
                    call("rm {}".format(rm_model), shell=True)
        else:
            if len(listdir("./models/train/")) == 0:
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                print("SOLO EJECUTA \"rasa train\"")
                exit()





