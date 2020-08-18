from subprocess import call
from os import listdir, chdir
import platform

def unpacking_tar():
    #Solo se hara en la computadora que se ellame "u1"... funciona en ubuntu
    if platform.node() == "u1":
        list_number = []
        for i in listdir("./models/"):
            print("PASO 9"*10)
            if i.find(".tar.gz") != -1:
                print("PASO 11" * 10)
                list_number.append(i[:8]+i[9:15])
        list_number = sorted(list_number)
        if len(list_number) >= 1:
            print("PASO 15" * 10)
            if len(listdir("models/train/")) > 0:
                print("PASO 17*" * 10)
                call("rm -r models/train/*", shell=True)
            print("PASO 19*" * 10)
            modelo = list_number[0][:8] + "-" + list_number[0][8:] + ".tar.gz"
            call("cp modelo /train/.")


            print("PASO 21*" * 10)
            chdir('models')
            print("PASO 23*" * 10)
            print("PASO 25*" * 10)
            call(" tar -xzvf {}".format(modelo), shell=True)
            print("PASO 27*" * 10)
            print("PASO 29*" * 10)
            print("PASO 31*" * 10)
            print("PASO 33*" * 10)
            print("PASO 35*" * 10)
            if len(list_number) > 1:
                print("PASO 27" * 10)
                for i in range(1,len(list_number)):
                    rm_model = list_number[i][:8] + "-" + list_number[i][8:] + ".tar.gz"
                    call("rm {}".format(rm_model), shell=True)
        else:
            print("PASO 32" * 10)
            if len(listdir("./models/train/")) == 0:
                print("PASO 34" * 10)
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                exit()





