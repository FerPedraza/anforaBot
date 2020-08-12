def hora(self):
    hora=datetime.now()
    if int(hora.strftime("%H")) in range(0,7):
        dia = 'de la madrugada'
    elif  int(hora.strftime("%H")) in range(7,12):
        dia = 'de la mañana'
    elif  int(hora.strftime("%H")) == 12:
        dia = 'del dia'
    elif  int(hora.strftime("%H")) in range(13,19):
        dia = 'de la tarde'
    else:
        dia = 'de la noche'
    mensaje = 'son las ' + hora.strftime("%H:%M:%S")+ ' hrs '+dia + ' hora del centro de México'
    return mensaje