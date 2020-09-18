
def validar_rfc(rfc,persona='fisica',paterno=None,materno=None,p_nombre=None,anio=None,mes=None,dia=None):
    rfc = rfc.replace("-","").strip().lower()
    if paterno:
        paterno = paterno.lower().strip()
    if materno:
        materno = materno.lower().strip()
    if p_nombre:
        p_nombre = p_nombre.lower().strip()
    if anio:
        anio = str(anio).strip()
    if mes:
        mes = str(mes).strip()
    if dia:
        dia = str(dia).strip()
    correct = False
    while True:

        if rfc.isalnum() == False:
            correct = False
            break
        if persona == "fisica":
            if len(rfc) != 13 and len(rfc) != 10:
                correct = False
                break
            if paterno and materno and p_nombre and anio and mes and dia:
                vocales = ['a','e','i','o','u']
                if rfc[0] != paterno[0]:
                    correct = False
                    break
                complete = False
                for i in range(len(paterno)):
                    if paterno[i] in vocales:
                        if paterno[i] != rfc[1]:
                            correct = False
                            complete = True
                            break
                        else:
                            break
                if complete == True:
                    break
                elif rfc[2] != materno[0]:
                    correct = False
                    break
                elif rfc[3] != p_nombre[0]:
                    correct = False
                    break
                elif rfc[4:6] != str(anio[-2:]):
                    correct = False
                    break
                elif rfc[6:8] != str(mes):
                    correct = False
                    break
                elif rfc[8:10] != str(dia):
                    correct = False
                    break
                else:
                    correct = True
                    break
            else:
                correct = True
                break
        if persona == "moral":
            if len(rfc) != 9 and len(rfc) != 12:
                correct = False
                break
            if p_nombre and anio and mes and dia:
                nombre = p_nombre.split()
                if len(nombre) >= 3:
                    if rfc[0] != nombre[0][0] or rfc[1] != nombre[1][0] or rfc[2] != nombre[2][0]:
                        correct = False
                        break
                if len(nombre) == 2 and len(nombre[1]) >= 2:
                    if rfc[0] != nombre[0][0] or rfc[1] != nombre[1][0] or rfc[2] != nombre[1][1]:
                        correct = False
                        break
                if len(nombre) == 1 and len(nombre) >= 3:
                    if rfc[0:3] != nombre[0:3]:
                        correct = False
                        break
                if rfc[3:5] != str(anio[-2:]):
                    correct = False
                    complete = True
                    break
                elif rfc[5:7] != str(mes):
                    correct = False
                    break
                elif rfc[7:9] != str(dia):
                    correct = False
                    break
                else:
                    correct = True
                    break
            else:
                correct = True
                break

    return correct

#print(validar_rfc("IAT030120E60",persona='moral',p_nombre='Industriales Acero Templado',anio="2003",mes='01',dia="20"))


