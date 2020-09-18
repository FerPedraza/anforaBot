
def classify_name(self, nombre_completo):
    nombre_completo_lista = nombre_completo.split()
    with open("validacion/data/data_names.txt") as file:
        nombres = file.read()
    for i in range(len(nombre_completo_lista)):
        if nombre_completo_lista[i] in nombres:
            nombre = nombre_completo_lista[i]
            nombre_completo_lista.pop(i)
            break
        else:
            nombre = nombre_completo_lista[0]
    if len(nombre_completo_lista) >= 2:
        paterno = nombre_completo_lista[0]
        materno = nombre_completo_lista[1]
    elif len(nombre_completo_lista) == 1:
        paterno = nombre_completo_lista[0]
        materno = ""
    else:
        paterno = ""
        materno = ""
    nombre = nombre[0].upper() + nombre[1:]
    paterno = paterno[0].upper() + paterno[1:]
    if materno != "":
        materno = materno[0].upper() + materno[1:]
    return nombre, paterno, materno