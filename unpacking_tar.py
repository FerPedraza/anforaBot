from subprocess import call
from os import listdir, chdir
import platform
import os
import tarfile

path_model = './models/train/'
path_nlu = './models/train/nlu'

BOTANFORA_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BOTANFORA_DIR, 'models')
MODELS_TRAIN_PATH = os.path.join(MODELS_PATH, 'train')
NLU_PATH = os.path.join(MODELS_TRAIN_PATH, 'nlu')



def unpacking_tar():
    #Desempaqueta en windows
    if platform.system() == "Windows":
        list_number = []
        for i in listdir(MODELS_PATH):
            if i.find(".tar.gz") != -1:
                list_number.append(i[:8]+i[9:15])
        list_number = sorted(list_number)
        if len(list_number) >= 1:
            if len(listdir(MODELS_TRAIN_PATH)) > 0:
                shell = 'rmdir /S /Q "' + MODELS_TRAIN_PATH + '"'
                call(shell, shell=True)
                shell = 'mkdir "' + MODELS_TRAIN_PATH + '"'
                call(shell, shell=True)
            modelo = list_number[-1][:8] + "-" + list_number[-1][8:] + ".tar.gz"
            print("MODELO: ",modelo)
            #call("ls", shell=True)
            path = "."
            MODEL_PATH = os.path.join(MODELS_PATH, modelo)
            tf = tarfile.open(MODEL_PATH)
            tf.extractall(path=MODELS_TRAIN_PATH)
            print("...extracted")
        else:
            if len(listdir(MODELS_TRAIN_PATH)) == 0:
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                print("SOLO EJECUTA \"rasa train\"")
                exit()
    # Desempaqueta en unix
    else:
        list_number = []
        for i in listdir("./models/"):
            if i.find(".tar.gz") != -1:
                list_number.append(i[:8] + i[9:15])
        list_number = sorted(list_number)
        if len(list_number) >= 1:
            if len(listdir("models/train/")) > 0:
                call("rm -r models/train/*", shell=True)
            modelo = list_number[-1][:8] + "-" + list_number[-1][8:] + ".tar.gz"
            print("MODELO: ",modelo)
            call("ls", shell=True)
            call("mv models/{} models/train/.".format(modelo), shell=True)
            chdir('models/train')
            call(" tar -xzvf {}".format(modelo), shell=True)
            chdir("../")
            lista_2 = listdir(".")
            for i in lista_2:
                if i.find(".tar.gz") != -1:
                    call("rm " + i, shell=True)
            chdir('../')
            print("...extracted")
        else:
            if len(listdir("./models/train/")) == 0:
                print("NO EXISTE MODELO EN EL DIRECTORIO TRAIN!!")
                print("SOLO EJECUTA \"rasa train\"")
                exit()
