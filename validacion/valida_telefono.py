
def validar_telefono(telefono):
    if len(telefono) == 10 and telefono.isdigit() == True:
        return True
    elif len(telefono) < 10:
        return False
    elif len(telefono) > 10 and telefono[0] == "+":
        var = telefono.split('+')
        if var[1].isdigit() == True:
            return True
        else:
            return False
    elif telefono.isalnum() == False:
        return False
    else:
        return False
