import asyncio
import pymongo
import pytz
import re
import platform

from text.limpia_texto import clean_text
from conversion.convierte_a_letras import convert_to_letters
from validacion.valida_telefono import validar_telefono
from text.limpia_texto import middle_clean_text
from validacion.valid_email import is_valid_email
from datetime import datetime, timedelta
from pprint import pprint


def menu_principal_salir(users):
    botones = [{'payload': 'saludar',
                'title': 'Regresar al menú inicial'},
               {'payload': 'salir',
                'title': 'Salir'}]
    for i in range(len(botones)):
        botones[i]['number'] = str(i + 1)
        botones[i]['letter number'] = convert_to_letters(i + 1)
    users['buttons'] = botones
    return users

"""


        if re.fullmatch("[\w\.]+@(?:\w\.)+\w+", text):
            intencion = "dar_correo"
            confianza = 0.99
        else:
            confianza = 0.1
"""


def valida_botones(speech, users):
    if "buttons" in speech[0].keys():
        botones = speech[0]['buttons']
        for i in range(len(botones)):
            botones[i]['number'] = str(i + 1)
            botones[i]['letter number'] = convert_to_letters(i + 1)
        users['buttons'] = botones
        print("ESTO VIENE DE 35")
        print(type(speech[0]['text']))
        print(type(botones))
        pprint(botones)
        print("lista")
        print([x['number'] + '. ' + x['title'] for x in botones])
        #mensaje = speech[0]['text']  + '\n'.join('@#AT#@@#OPTION#@' + [x['number'] + '. ' + x['title'] for x in botones]).format(
        #    nombre=users['name'])
        print(type(speech[0]['text']))
        mensaje = speech[0]['text']
        lista = [x['number'] + '. ' + x['title'] for x in botones]
        for i in range(len(lista)):
            mensaje = mensaje + '@#AT#@@#OPTION#@\n' + lista[i]
        #mensaje = speech[0]['text'] + '@#AT#@@#OPTION#@\n'.join(
        #     [x['number'] + '. ' + x['title'] for x in botones])
        print("esto es 43")
        print(mensaje)
        #print('mensaje de valida botones', mensaje)
    else:
        mensaje = speech[0]['text'].format(nombre=users['name'])
    return mensaje, users


class SmartBot:
    def __init__(self, facebook=False):
        if platform.node() == "u1" or platform.node() == "DESKTOP-0CKRHA6" or platform.node() == "karma":
            ip = "localhost"
        else:
            ip = "172.17.0.9"
        b_client = pymongo.MongoClient(ip, 27017) #serv mongo 10.100.13.20 #docker 172.17.0.8
        db = b_client['Bots']
        self.colection = db['Anfora']
        self.facebook = facebook

    def bot(self, text, users):
        bandera_botones = False
        if users['buttons']:
            # Las siguientes 5 lineas son para verificar que si se introdujo un número, este se encuentre dentro
            # del rango de opciones de botones que se tienen, de lo contrario soltará un mensaje de error.
            num_btns = [x.get('payload') for x in users['buttons']]
            if self.original_text.isdigit() and num_btns and int(self.original_text) < 9:
                if len(num_btns) < int(self.original_text):
                    mensaje = '@#AT#@@#TITLE#@Lo siento no entendí qué quisiste decir, por favor introduce una opción válida' \
                        + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                        + "@#AT#@@#OPTION#@\n2. Salir👋"
                    users = menu_principal_salir(users)
                    return mensaje, users
            # El siguiente if sirve para validar si la entrada recibida (text) hace referencia a un boton del mensaje
            # anterior, ya sea como número o texto.
            option = [x['payload'] for x in users['buttons'] if
                      str(clean_text(text)).lower() in map(lambda valor: valor.lower(), x.values())]
            if option:
                text = option[0]
                bandera_botones = True
        text = middle_clean_text(text)
        speech = self.extraer_texto(text)
        NLU = self.extraer_intenciones(text)
        intencion = NLU['intent']['name']
        confianza = NLU['intent']['confidence']
        print("#" * 30)
        print(intencion)
        print(confianza)
        print(speech)
        print("This is users")
        print(users)
        print("#" * 30)
        self.save_info(None, None, None, None)
        # Aqui se limpia el texto si no esta dentro de intenciones particulares
        # Aqui se guarda informacion de alguna opcion del menú principal sin que implique respuesta al usuario
        
        print("dewdwedoqweiiuqewhiuewqd")
        print("------------------------")
        print(text)
        

        if re.fullmatch("[\w\.]+@(?:\w+\.)+\w+", text):
            print("Correo valido--------------------")
            intencion = "dar_correo"
            confianza = 0.99

        if intencion == "sucursales" or intencion == "tienda_linea" or intencion == "cotizaciones" \
                or intencion == "promociones" or intencion == "mensaje_covid":
            tz = pytz.timezone('America/Mexico_City')
            ct = datetime.now(tz=tz).replace(tzinfo=None)
            self.update_request(campo="menu_principal", valor=intencion, date=ct)
        elif intencion == "quiero_comprar" or intencion == "rastrear_pedido" or intencion == "problema_pedido" \
                or intencion == "cancelar_pedido":
            tz = pytz.timezone('America/Mexico_City')
            ct = datetime.now(tz=tz).replace(tzinfo=None)
            self.update_request(campo="menu_tienda_linea", valor=intencion, date=ct)
        if users['name'] == 'Humano':
            # Este if evalua la confianza del texto, si es una frase o palabra diferente a las del entrenamiento
            # la tomara como que no la conoce y se ejecutará esta parte del codigo.
            if confianza < 0.55 and intencion != "dar_correo" and intencion != "dar_numero" \
                    and intencion != "agente_quiero_comprar" and intencion != "problema_pedido":
                mensaje, users = self.saludar(users)

                return mensaje, users
            # Se despliegan todas las intenciones dinamicas
            elif intencion == "saludar":
                mensaje, users = self.saludar(users)
                self.save_info(text, mensaje, NLU, users['buttons'])
                return mensaje, users

            elif intencion == "mexico" or intencion == "ciudad_de_mexico" or intencion == "queretaro" \
                    or intencion == "veracruz" or intencion == "hidalgo" or intencion == "guanajuato" \
                    or intencion == "chiapas" or intencion == "toluca":
                estado = intencion
                menu_tienda_linea = self.colection.find_one({"user_id": self.main_user}).get("request")\
                    .get("menu_tienda_linea").get('opcion')
                if estado == "toluca":
                    if menu_tienda_linea != "quiero_comprar":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\n  Almacenes Anfora – *San Lorenzo*" \
                              + "\n🏨Alfredo del Mazo 702, Delegación San Lorenzo Tepaltitlán, C.P. 50010 Toluca de " \
                                "Lerdo" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n" + "  Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞722 237 3726" \
                              + "\nhttps://goo.gl/maps/zDJf14V9xunFWY7z7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Metepec*" \
                              + "\n🏨Av. Pino Suárez 2400-A, Fraccionamiento Xinantécatl,  C.P. 52140 Metepec" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n" + "  Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞722 280 1254" \
                              + "\nhttps://goo.gl/maps/sxBQrqSNiZXDS1xQ7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Tenancingo*" \
                              + "\n🏨Guadalupe Victoria 105, Centro Tenancingo, C.P. 52400 Tenancingo" \
                              + "\n🕑Lunes, martes, miércoles y viernes" \
                              + "\n  10:00 am a 8:00 pm" \
                              + "\n  Jueves y Sábado: 09:00 am a 8:00 pm" \
                              + "\n   Domingos: de 9:00 am a 7:00 pm" \
                              + "\n📞714 142 3190" \
                              + "\nhttps://goo.gl/maps/F7n9oQrE2Z3zZ3Rp6" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Zinacantepec*" \
                              + "\n🏨PASEO ADOLFO LÓPEZ MATEOS No. 1608, COLONIA, San Mateo Oxtotitlán, C.P. 50100 " \
                                "Toluca de Lerdo" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞 722 278 5136" \
                              + "\nhttps://goo.gl/maps/GqiyQEUUB3Hwgodq7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Juárez 1*" \
                              + "\n🏨Av. Juárez Sur 119, Centro, C.P. 50000 Toluca, Estado de México" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n  Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞722 214 0284" \
                              + "\nhttps://goo.gl/maps/cq4QiTQcfGPXXnwM6" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Juárez 2*" \
                              + "\n🏨Av. Juárez Sur No. 206 Colonia Centro, Toluca,  Estado de México C.P. 50000" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n📞722 214 2800" \
                              + "\nhttps://goo.gl/maps/5fMLvGdy1xDSm9yS9" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Portales*" \
                              + "\n🏨Portal 20 de Noviembre No. 109 interiores D Y C Colonia  Centro C.p. 50000 Toluca" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞722 213 5054" \
                              + "\nhttps://goo.gl/maps/geaW5KTeD4166FS8A" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Terminal*" \
                              + "\n🏨Avenida Paseo Tollocan 501, Américas Cárdenas, 50130 Toluca de Lerdo" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞722 212 9731" \
                              + "\nhttps://goo.gl/maps/p7DgbEUF3yFhYDmP6" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"

                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\n  Almacenes Anfora – *San Lorenzo*" \
                                  + "\n🏨Alfredo del Mazo 702, Delegación San Lorenzo Tepaltitlán, C.P. 50010 Toluca " \
                                    "de Lerdo" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n" + "  Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞722 237 3726" \
                                  + "\nhttps://goo.gl/maps/zDJf14V9xunFWY7z7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Metepec*" \
                                  + "\n🏨Av. Pino Suárez 2400-A, Fraccionamiento Xinantécatl,  C.P. 52140 Metepec" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n" + "  Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞722 280 1254" \
                                  + "\nhttps://goo.gl/maps/sxBQrqSNiZXDS1xQ7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Tenancingo*" \
                                  + "\n🏨Guadalupe Victoria 105, Centro Tenancingo, C.P. 52400 Tenancingo" \
                                  + "\n🕑Lunes, martes, miércoles y viernes" \
                                  + "\n  10:00 am a 8:00 pm" \
                                  + "\n  Jueves y Sábado: 09:00 am a 8:00 pm" \
                                  + "\n   Domingos: de 9:00 am a 7:00 pm" \
                                  + "\n📞714 142 3190" \
                                  + "\nhttps://goo.gl/maps/F7n9oQrE2Z3zZ3Rp6" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Zinacantepec*" \
                                  + "\n🏨PASEO ADOLFO LÓPEZ MATEOS No. 1608, COLONIA, San Mateo Oxtotitlán, C.P. " \
                                    "50100 Toluca de Lerdo" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞 722 278 5136" \
                                  + "\nhttps://goo.gl/maps/GqiyQEUUB3Hwgodq7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Juárez 1*" \
                                  + "\n🏨Av. Juárez Sur 119, Centro, C.P. 50000 Toluca, Estado de México" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n  Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞722 214 0284" \
                                  + "\nhttps://goo.gl/maps/cq4QiTQcfGPXXnwM6" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Juárez 2*" \
                                  + "\n🏨Av. Juárez Sur No. 206 Colonia Centro, Toluca,  Estado de México C.P. 50000" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n📞722 214 2800" \
                                  + "\nhttps://goo.gl/maps/5fMLvGdy1xDSm9yS9" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Portales*" \
                                  + "\n🏨Portal 20 de Noviembre No. 109 interiores D Y C Colonia  Centro C.p. 50000 Toluca" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞722 213 5054" \
                                  + "\nhttps://goo.gl/maps/geaW5KTeD4166FS8A" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Terminal*" \
                                  + "\n🏨Avenida Paseo Tollocan 501, Américas Cárdenas, 50130 Toluca de Lerdo" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞722 212 9731" \
                                  + "\nhttps://goo.gl/maps/p7DgbEUF3yFhYDmP6" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif estado == "ciudad_de_mexico":
                    if menu_tienda_linea != "quiero_comprar":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *Lopez*" \
                              + "\n🏨LOPEZ No. 50 COLONIA CENTRO DELEGACION CUAUHTEMOC C.P. 06050" \
                              + "\n🕑Lunes a Sábado: 9:30 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5130 3280" \
                              + "\nhttps://goo.gl/maps/hwG7vmZA6tiSUvMe7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Aranda*" \
                              + "\n🏨ARANDA No. 18 o AYUNTAMIENTO No. 15 COLONIA CENTRO DELEGACION CUAUHTEMOC " \
                              + "C.P.06050" \
                              + "\n🕑Lunes a Sábado: 9:30 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5518 0290" \
                              + "\nhttps://goo.gl/maps/hwG7vmZA6tiSUvMe7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Artículo 123*" \
                              + "\n🏨ARTICULO 123 No. 10 COLONIA CENTRO C.P.06050 DELGACION CUAUHTEMOC" \
                              + "\n🕑Lunes a Sábado: 9:00 am a 7:00 pm" \
                              + "\n   Domingo: 10:30 am a 6:30 pm" \
                              + "\n📞55 5512 6509" \
                              + "\nhttps://goo.gl/maps/3yCGdHPefD2kLhh98" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Tacubaya*" \
                              + "\n🏨ANTONIO MACEO No. 27 COLONIA TACUBAYA C.P.11870 MIGUEL HIDALGO" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5271 8799" \
                              + "\nhttps://goo.gl/maps/ZUZHYEg7B7CmQvt26" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *Lopez*" \
                                  + "\n🏨LOPEZ No. 50 COLONIA CENTRO DELEGACION CUAUHTEMOC C.P. 06050" \
                                  + "\n🕑Lunes a Sábado: 9:30 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5130 3280" \
                                  + "\nhttps://goo.gl/maps/hwG7vmZA6tiSUvMe7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Aranda*" \
                                  + "\n🏨ARANDA No. 18 o AYUNTAMIENTO No. 15 COLONIA CENTRO DELEGACION CUAUHTEMOC " \
                                  + "C.P.06050" \
                                  + "\n🕑Lunes a Sábado: 9:30 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5518 0290" \
                                  + "\nhttps://goo.gl/maps/hwG7vmZA6tiSUvMe7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Artículo 123*" \
                                  + "\n🏨ARTICULO 123 No. 10 COLONIA CENTRO C.P.06050 DELGACION CUAUHTEMOC" \
                                  + "\n🕑Lunes a Sábado: 9:00 am a 7:00 pm" \
                                  + "\n   Domingo: 10:30 am a 6:30 pm" \
                                  + "\n📞55 5512 6509" \
                                  + "\nhttps://goo.gl/maps/3yCGdHPefD2kLhh98" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Tacubaya*" \
                                  + "\n🏨ANTONIO MACEO No. 27 COLONIA TACUBAYA C.P.11870 MIGUEL HIDALGO" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5271 8799" \
                                  + "\nhttps://goo.gl/maps/ZUZHYEg7B7CmQvt26" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"
                elif intencion == "mexico":
                    if menu_tienda_linea != "quiero_comprar":
                    #if mp != "tienda_linea":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\n  Almacenes Anfora – *Ecatepec*" \
                              + "\n🏨Blvd. Insurgentes Esq. Emiliano Zapata locales 02 Y 03, San Cristóbal Centro, " \
                                "55000 Ecatepec de Morelos" \
                              + "\n🕑Lunes a Sábado: 9:30 am a 7:30 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5787 0911" \
                              + "\nhttps://goo.gl/maps/x7gwmaFufip9xC4u8" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Atizapán*" \
                              + "\n🏨Carretera Atizapán Nicolas Romero Esq. Av Adolfo López Mateos 11, Local 6A y 7, " \
                              + "El Pedregal de Atizapán, 52948 Atizapán De Zaragoza" \
                              + "\n🕑Lunes a Sábado: 9:00 am a 7:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5077 7316" \
                              + "\nhttps://goo.gl/maps/KjpQmnsW2P6BpwtM7" \
                              + "\n" \
                              + "\n  Almacenes Anfora – *Chalco*" \
                              + "\n🏨Av. Nacional no.57 Col. San Sebastian Mpio. De Chalco, Estado de México, " \
                                "C.P.  56600" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞55 5982 8368 y 55 3092 1009" \
                              + "\nhttps://goo.gl/maps/mE3xzUmgmTZLT7GQ7" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\n  Almacenes Anfora – *Ecatepec*" \
                                  + "\n🏨Blvd. Insurgentes Esq. Emiliano Zapata locales 02 Y 03, San Cristóbal Centro, " \
                                    "55000 Ecatepec de Morelos" \
                                  + "\n🕑Lunes a Sábado: 9:30 am a 7:30 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5787 0911" \
                                  + "\nhttps://goo.gl/maps/x7gwmaFufip9xC4u8" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Atizapán*" \
                                  + "\n🏨Carretera Atizapán Nicolas Romero Esq. Av Adolfo López Mateos 11, Local 6A y 7, " \
                                  + "El Pedregal de Atizapán, 52948 Atizapán De Zaragoza" \
                                  + "\n🕑Lunes a Sábado: 9:00 am a 7:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5077 7316" \
                                  + "\nhttps://goo.gl/maps/KjpQmnsW2P6BpwtM7" \
                                  + "\n" \
                                  + "\n  Almacenes Anfora – *Chalco*" \
                                  + "\n🏨Av. Nacional no.57 Col. San Sebastian Mpio. De Chalco, Estado de México, " \
                                    "C.P.  56600" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞55 5982 8368 y 55 3092 1009" \
                                  + "\nhttps://goo.gl/maps/mE3xzUmgmTZLT7GQ7" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif intencion == "queretaro":
                    if menu_tienda_linea != "quiero_comprar":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *Querétaro Zaragoza*" \
                              + "\n🏨Calle Ignacio Zaragoza 41, El Carrizal, 76030 Santiago de Querétaro, QRO" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞442 193 5585" \
                              + "\nhttps://goo.gl/maps/T5age1xc4Tks7Zzr5" \
                              + "\n" \
                              + "\nAlmacenes Anfora – *Querétaro Alameda*" \
                              + "\n🏨Avenida Michoacán No 119, Colonia Centro, 76000 Querétaro, Qro." \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞442 483 3429" \
                              + "\nhttps://goo.gl/maps/tgG117iksdk1qtEB9" \
                              + "\n" \
                              + "\nAlmacenes Anfora – *San Juan del Río*" \
                              + "\n🏨Boulevard Hidalgo 66, Colonia Centro San Juan del Río, San Juan Del Río " \
                                "Querétaro, México, C.P. 76800" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞427 272 5539" \
                              + "\nhttps://goo.gl/maps/GqhpTyNky91KUbXu6" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *Querétaro Zaragoza*" \
                                  + "\n🏨Calle Ignacio Zaragoza 41, El Carrizal, 76030 Santiago de Querétaro, QRO" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞442 193 5585" \
                                  + "\nhttps://goo.gl/maps/T5age1xc4Tks7Zzr5" \
                                  + "\n" \
                                  + "\nAlmacenes Anfora – *Querétaro Alameda*" \
                                  + "\n🏨Avenida Michoacán No 119, Colonia Centro, 76000 Querétaro, Qro." \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞442 483 3429" \
                                  + "\nhttps://goo.gl/maps/tgG117iksdk1qtEB9" \
                                  + "\n" \
                                  + "\nAlmacenes Anfora – *San Juan del Río*" \
                                  + "\n🏨Boulevard Hidalgo 66, Colonia Centro San Juan del Río, San Juan Del Río " \
                                    "Querétaro, México, C.P. 76800" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞427 272 5539" \
                                  + "\nhttps://goo.gl/maps/GqhpTyNky91KUbXu6" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif intencion == "veracruz":
                    if menu_tienda_linea != "quiero_comprar":
                    #if mp != "tienda_linea":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *Orizaba*" \
                              + "\n🏨AVENIDA ORIENTE 4 No. 40 COLONIA CENTRO, ORIZABA VERACRUZ C.P.94300" \
                              + "\n🕑Lunes a Sábado: 10:30 am a 8:30 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞272 725 8495" \
                              + "\nhttps://goo.gl/maps/rraVWVcLLAcfkAAC9" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *Orizaba*" \
                                  + "\n🏨AVENIDA ORIENTE 4 No. 40 COLONIA CENTRO, ORIZABA VERACRUZ C.P.94300" \
                                  + "\n🕑Lunes a Sábado: 10:30 am a 8:30 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞272 725 8495" \
                                  + "\nhttps://goo.gl/maps/rraVWVcLLAcfkAAC9" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif intencion == "hidalgo":
                    if menu_tienda_linea != "quiero_comprar":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *Tula de Allende*" \
                              + "\n🏨ALLE LEANDRO VALLE NO. 102 PLANTA BAJA, COL. CENTRO, MPIO. TULA DE ALLENDE, " \
                              + "ESTADO DE HIDALGO, C.P. 42800" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞773 732 6127 y 773 732 7036" \
                              + "\nhttps://goo.gl/maps/GcU5pGPhQQKk8FyQ7" \
                              + "\n" \
                              + "\nAlmacenes Anfora – *Tulancingo*" \
                              + "\n🏨CALLE SAN LUIS POTOSI NO. 101 ESQUINA. AV. 21 DE MARZO COL. VICENTE GUERRERO " \
                              + "MPIO. TULANCINGO DE BRAVO ESTADO DE HIDALGO C.P. 43630" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞775 112 0414" \
                              + "\nhttps://goo.gl/maps/qf2j6CG4p1Mfc5D26" \
                              + "\n" \
                              + "\nAlmacenes Anfora – *Pachuca*" \
                              + "\n🏨AVENIDA JUAREZ No. 501 COLONIA PERIODISTA ,PACHUCA DE SOTO HIDALGO C.P.:42060" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 11:00 am a 6:00 pm" \
                              + "\n📞771 718 1868" \
                              + "\nhttps://goo.gl/maps/GpPgW2Hs2871g4eD7" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *Tula de Allende*" \
                                  + "\n🏨ALLE LEANDRO VALLE NO. 102 PLANTA BAJA, COL. CENTRO, MPIO. TULA DE ALLENDE, " \
                                  + "ESTADO DE HIDALGO, C.P. 42800" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞773 732 6127 y 773 732 7036" \
                                  + "\nhttps://goo.gl/maps/GcU5pGPhQQKk8FyQ7" \
                                  + "\n" \
                                  + "\nAlmacenes Anfora – *Tulancingo*" \
                                  + "\n🏨CALLE SAN LUIS POTOSI NO. 101 ESQUINA. AV. 21 DE MARZO COL. VICENTE GUERRERO " \
                                  + "MPIO. TULANCINGO DE BRAVO ESTADO DE HIDALGO C.P. 43630" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞775 112 0414" \
                                  + "\nhttps://goo.gl/maps/qf2j6CG4p1Mfc5D26" \
                                  + "\n" \
                                  + "\nAlmacenes Anfora – *Pachuca*" \
                                  + "\n🏨AVENIDA JUAREZ No. 501 COLONIA PERIODISTA ,PACHUCA DE SOTO HIDALGO C.P.:42060" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 11:00 am a 6:00 pm" \
                                  + "\n📞771 718 1868" \
                                  + "\nhttps://goo.gl/maps/GpPgW2Hs2871g4eD7" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif intencion == "guanajuato":
                    if menu_tienda_linea != "quiero_comprar":
                    #if mp != "tienda_linea":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *León Centro*" \
                              + "\n🏨Calle Belisario Domínguez, Col. León de los Aldamas Centro, León, Guanajuato, " \
                                "CP 37000" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞 477 713 3220 y 477 713 3060" \
                              + "\nhttps://goo.gl/maps/PsJnizTzTi8U7kBS9" \
                              + "\n" \
                              + "\nAlmacenes Anfora – *León Delta*" \
                              + "\n🏨Blvd. Delta 101, Col. Fracc. Industrial Delta, León, Guanajuato, CP 37545" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞 477 167 5629 y 477 761 2379" \
                              + "\nhttps://goo.gl/maps/tKjk3fR62Gjok5FDA" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *León Centro*" \
                                  + "\n🏨Calle Belisario Domínguez, Col. León de los Aldamas Centro, León, Guanajuato, " \
                                    "CP 37000" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞 477 713 3220 y 477 713 3060" \
                                  + "\nhttps://goo.gl/maps/PsJnizTzTi8U7kBS9" \
                                  + "\n" \
                                  + "\nAlmacenes Anfora – *León Delta*" \
                                  + "\n🏨Blvd. Delta 101, Col. Fracc. Industrial Delta, León, Guanajuato, CP 37545" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞 477 167 5629 y 477 761 2379" \
                                  + "\nhttps://goo.gl/maps/tKjk3fR62Gjok5FDA" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"

                elif intencion == "chiapas":
                    if menu_tienda_linea != "quiero_comprar":
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                              + "\nAlmacenes Anfora – *Tuxtla Gutiérrez*" \
                              + "\n🏨11A Oriente Norte 221, Col. Hidalgo, Tuxtla Gutiérrez, Chiapas, CP 29040" \
                              + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                              + "\n   Domingo: 10:00 am a 6:00 pm" \
                              + "\n📞961 600 0610 y 961 346 7160" \
                              + "\nhttps://goo.gl/maps/3ZkxsGaAX4SdS9CS6" \
                              + "\n" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    else:
                        mensaje = "@#AT#@@#TITLE#@¡Estas son las sucursales cercanas a ti!" \
                                  + "\nAlmacenes Anfora – *Tuxtla Gutiérrez*" \
                                  + "\n🏨11A Oriente Norte 221, Col. Hidalgo, Tuxtla Gutiérrez, Chiapas, CP 29040" \
                                  + "\n🕑Lunes a Sábado: 10:00 am a 8:00 pm" \
                                  + "\n   Domingo: 10:00 am a 6:00 pm" \
                                  + "\n📞961 600 0610 y 961 346 7160" \
                                  + "\nhttps://goo.gl/maps/3ZkxsGaAX4SdS9CS6" \
                                  + "\n" \
                                  + "\nAhora ingresa tu sucursal mas cercana para continuar con tu compra" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir👋"
                else:
                    mensaje = "@#AT#@@#TITLE#@Por el momento, no contamos con sucursal en tu estado ☹. ¡Compra en https://www.almacenesanfora.com/, contamos con envió a toda la Republica Mexicana! 🚚" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                users = menu_principal_salir(users)
                return mensaje, users

            elif intencion == "decir_sucursal":

                mensaje = "@#AT#@@#TITLE#@Por favor compárteme tu número de teléfono a 10 dígitos" \
                          + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                          + "@#AT#@@#OPTION#@\n2. Salir"
                users = menu_principal_salir(users)
                return mensaje, users

            elif intencion == "mensaje_covid":
                mensaje = "@#AT#@@#IMG#@https://www.broadcasterbot.com/cliente/almacenesanfora/0001.jpg" \
                          + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                          + "@#AT#@@#OPTION#@\n2. Salir"
                users = menu_principal_salir(users)
                return mensaje, users

            elif intencion == "dar_numero":
                mtl0 = self.colection.find_one({"user_id": self.main_user}).get("request").get("menu_tienda_linea")
                mtl = mtl0.get("opcion")
                date = mtl0.get("date")
                tz = pytz.timezone('America/Mexico_City')
                ct_now = datetime.now(tz=tz).replace(tzinfo=None)

                if mtl == "quiero_comprar" and ct_now - date < timedelta(minutes=5) and text.isdigit():
                    if validar_telefono(text):
                        mensaje = "@#AT#@@#TITLE#@Por favor compárteme tu correo electrónico" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir"
                    else:
                        mensaje = "@#AT#@@#TITLE#@Vuelve a introducir tu número por favor" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir"
                    users = menu_principal_salir(users)
                elif mtl == "rastrear_pedido" and ct_now - date < timedelta(minutes=5) and text.isdigit():
                    if len(text) == 8:
                        self.update_request('numero_orden', )
                        mensaje = "En seguida te contactaré con un agente de Ventas @#AT#@@#DELEGATE#@"
                    else:
                        mensaje = "@#AT#@@#TITLE#@Ingresa nuevamente tu N° de orden por favor" \
                                  + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                                  + "@#AT#@@#OPTION#@\n2. Salir"
                        users = menu_principal_salir(users)
                elif mtl == "problema_pedido" and text.isdigit():
                    mensaje = "@#AT#@@#TITLE#@En seguida te contactaré con un agente de Ventas @#AT#@@#DELEGATE#@"
                elif mtl == "cancelar_pedido" and text.isdigit():
                    if self.laboral():
                        mensaje = "@#AT#@@#TITLE#@En seguida te contactaré con un agente de Ventas @#AT#@@#DELEGATE#@"
                    else:
                        mensaje = "@#AT#@@#TITLE#@Hemos recibido tu mensaje y una persona te atenderá lo antes posible. Nuestros " \
                                  "horarios de servicio son de Lunes a Sábado de 0 8: 00 am a 05: 00 pm. " \
                                  " @#AT#@@#DELEGATE#@"
                else:
                    mensaje, users = self.saludar(users)
                    users = menu_principal_salir(users)

                return mensaje, users

            elif intencion == "dar_fecha_nacimiento":
                mtl = self.colection.find_one({"user_id": self.main_user}).get("request").get("menu_tienda_linea") \
                    .get("opcion")
                lista = text.split()
                if len(lista) == 3:
                    if lista[0].isdigit() and lista[1].isalpha() and lista[2].isdigit():
                        valido = True
                    else:
                        valido = False
                elif len(lista) == 5:
                    if lista[0].isdigit() and lista[1].isalpha() and lista[2].isalpha() and lista[3].isalpha() and \
                            lista[4].isdigit():
                        valido = True
                    else:
                        valido = False
                else:
                    valido = False
                if mtl == "rastrear_pedido" and valido:
                    if valido:
                        # aqui va un ws
                        mensaje = "@#AT#@@#TITLE#@Hemos recibido tu fecha de nacimiento, estamos buscando tu pedido 🔎 \n¡Espera un " \
                                  "momento! "
                        mensaje = mensaje + "\nTu pedido ya está listo. 👇 \n¡Gracias por utilizar este servicio!" \
                            + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                            + "@#AT#@@#OPTION#@\n2. Salir👋"
#                        mensaje si no esta el pedido
#                        Almacenes Anfora: A tu pedido le falta un poco más de tiempo, ten paciencia, por f
                elif mtl == "problema_pedido" and valido:
                    mensaje = " @#AT#@@#DELEGATE#@"
                else:
                    mensaje = "@#AT#@@#TITLE#@Vuelve a ingresar tu fecha de nacimiento por favor" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                users = menu_principal_salir(users)
                return mensaje, users

            elif intencion == "promociones":
                tz = pytz.timezone('America/Mexico_City')
                ct = datetime.now(tz=tz)
                day = ct.day
                if day <= 16:
                    mensaje = "@#AT#@@#TITLE#@En seguida te contactaré con un agente de Ventas @#AT#@@#IMG#@https://www.broadcasterbot.com/cliente/almacenesanfora/1q.jpg " \
                          " @#AT#@@#DELEGATE#@"
                else:
                    mensaje = "@#AT#@@#TITLE#@En seguida te contactaré con un agente de Ventas @#AT#@@#IMG#@https://www.broadcasterbot.com/cliente/almacenesanfora/2q.jpg" \
                              " @#AT#@@#DELEGATE#@"
                return mensaje, users

            elif intencion == "dar_correo":
                print("--------------------------")
                print(text)
                if is_valid_email(text):
                    print("CORREO ES VALIDO")
                    mensaje = "@#AT#@@#TITLE#@¡Perfecto! 👏, Prepárate 📝" \
                              + "💡 TIP: Puedes mandar la foto de tu lista con el nombre de cada artículo y cantidad " \
                                "que " \
                              + "necesitas (piezas)." \
                                " Un agente tomará tu pedido ¿Estás listo?" \
                              + "@#AT#@@#OPTION#@\n1. Si" \
                              + "@#AT#@@#OPTION#@\n2. No" \
                              + "@#AT#@@#OPTION#@\n3. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n4. Salir👋"
                    botones = [{'payload': 'agente_quiero_comprar',
                                'title': 'Si'},
                               {'payload': 'saludar',
                                'title': 'No'},
                               {'payload': 'saludar',
                                'title': 'Regresar al menú inicial🔙'},
                               {'payload': 'salir',
                                'title': 'Salir👋'}]
                    for i in range(len(botones)):
                        botones[i]['number'] = str(i + 1)
                        botones[i]['letter number'] = convert_to_letters(i + 1)
                    users['buttons'] = botones
                else:
                    mensaje = "@#AT#@@#TITLE#@Vuelve a ingresar tu correo por favor" \
                              + "@#AT#@@#OPTION#@\n1. Regresar al menú principal🔙" \
                              + "@#AT#@@#OPTION#@\n2. Salir👋"
                    users = menu_principal_salir(users)
                return mensaje, users

            elif intencion == "agente":
                laboral = self.laboral()
                if laboral:
                    mensaje = "@#AT#@@#TITLE#@Comunicando con un operador @#AT#@@#DELEGATE#@"
                else:
                    mensaje = "@#AT#@@#TITLE#@Hemos recibido tu mensaje y una persona te atenderá lo antes posible. Nuestros " \
                              "horarios de servicio son de Lunes a Sábado de 0 8: 00 am a 05: 00 pm. " \
                              " @#AT#@@#DELEGATE#@"
                return mensaje, users

        mensaje = ''
        if bandera_botones:
            users['buttons'] = []
        if speech:
            mensaje, users = valida_botones(speech, users)
            print("THIS IS MESSAGE FROM VALIDA BOTONES")
            print(mensaje)
        var = re.compile("{nombre}")
        if re.search(var, mensaje):
            mensaje = mensaje.format(nombre=users['name'])
            print("this is mesaje form 757")
            print(mensaje)
        #self.save_info(text, mensaje, NLU, users['buttons'])
        print("*" * 40)
        print("USERS")
        print(users)
        print("TEXT")
        print(text)
        print("SPEECH")
        print(speech)
        print("INTENCION")
        print(intencion)
        print("CONFIANZA")
        print(confianza)
        print("*" * 40)
        # save info
        return mensaje, users

    def extraer_intenciones(self, text):
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        NLU = loop1.run_until_complete(self.interpreter.parse(text))
        return NLU

    def extraer_texto(self, text):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        speech = loop.run_until_complete(self.agent.handle_text(text))
        return speech

    def save_info(self, text, respuesta, NLU, buttons):

        d = self.colection.find_one({"user_id": self.main_user})
        if NLU:
            intent = NLU['intent']['name']
            confidence = NLU['intent']['confidence']
        else:
            intent = None
            confidence = None
        if not d:
            if respuesta == "Lo siento no entendí qué quisiste decir, por favor introduce una opción válida":
                br = self.colection.find_one({"user_id": self.main_user}).get("request").get("bad_requests")
                br_n = {'botones': pytz.utc.localize(datetime.utcnow())}
                br.append(br_n)

            if self.main_user.isdigit():
                plataforma = "whatsapp"
            else:
                ls = self.main_user.split("+")
                if len(ls) == 2 and ls[1].isdigit():
                    plataforma = "whatsapp"
                else:
                    plataforma = "facebook"

            date = pytz.utc.localize(datetime.utcnow())
            doc = {'user_id': self.main_user,
                   'platform': plataforma,
                   'history': {'user': [{'date': date, 'text': text, 'intent': intent, 'confidence': confidence}],
                               'bot': [{'date': date, 'text': respuesta, 'buttons': buttons}],
                               'last_bot': {'date': date, 'text': respuesta, 'buttons': buttons},
                               'last_user': {'date': date, 'text': text, 'intent': intent, 'confidence': confidence}
                               },
                   'request': {'numero_orden': None,
                               'nombre': None,
                               'telefono': None,
                               'compania': None,
                               'correo': None,
                               'rfc': None,
                               'menu_principal': {'opcion': None, 'date': None},
                               'menu_tienda_linea': {'opcion': None, 'date': None},
                               'municipio': None,
                               'ciudad': None,
                               'estado': None,
                               'coordinates': {'type': 'Point', 'coordinates': [None, None]},
                               'otros_datos_rfc': [],
                               'bad_requests': [],
                               'nombre_rfc': None,
                               'paterno_rfc': None,
                               'materno_rfc': None,
                               'status': 'incomplete'},
                   'intents_history': [intent],
                   'request_history': [],
                   'conversation': [{"date": date, "user": text, "bot": respuesta}],
                   'num_requests': 0
                   }
            self.colection.insert_one(doc)

        else:
            conv_u = d['history']['user']
            date = pytz.utc.localize(datetime.utcnow())
            conv_u.append({'date': date, 'text': text, 'intent': intent, 'confidence': confidence})
            conv_b = d['history']['bot']
            conv_b.append({'date': date, 'text': respuesta, 'buttons': buttons})
            int_hist = d['intents_history']
            int_hist.append(intent)
            if respuesta == "Lo siento no entendí qué quisiste decir, por favor introduce una opción válida":
                br = self.colection.find_one({"user_id": self.main_user}).get("request").get("bad_requests")
                br.append(date)
            else:
                br = self.colection.find_one({"user_id": self.main_user}).get("request").get("bad_requests")
            c = self.colection.find_one({"user_id": self.main_user}).get("conversation")

            c.append({"date": date, "user": text, "bot": respuesta})
            self.colection.update_one({"user_id": self.main_user}, {'$set': {'history.user': conv_u,
                                                                             'history.bot': conv_b,
                                                                             'history.last_bot': {'date': date,
                                                                                                  'text': respuesta,
                                                                                                  'buttons': buttons},
                                                                             'history.last_user': {'date': date,
                                                                                                   'text': text,
                                                                                                   'intent': intent,
                                                                                                   'confidence':
                                                                                                       confidence},
                                                                             'intents_history': int_hist,
                                                                             'request.bad_requests': br,
                                                                             'conversation': c  # este no
                                                                             }})

    def update_request(self, campo, valor=None, date=None):

        d = self.colection.find_one({'user_id': self.main_user})
        if d:
            if campo == 'request_history' or campo == 'num_requests':
                self.colection.update_one({'user_id': self.main_user}, {'$set': {campo: valor}})
            elif campo == 'menu_principal' or campo == 'menu_tienda_linea':
                self.colection.update_one({'user_id': self.main_user}, {
                    '$set': {'request.' + campo + '.opcion': valor, 'request.' + campo + '.date': date}})

            elif campo == "bad_requests":
                br = self.colection.find_one({"user_id": self.main_user}).get("request").get("bad_requests")
                br.append({valor: date})
                self.colection.update_one({'user_id': self.main_user}, {'$set': {'request.' + campo: br}})
            elif campo == 'otros_datos_rfc':
                odr = self.colection.find_one({"user_id": self.main_user}).get("request").get("otros_datos_rfc")
                odr.append(date)
                self.colection.update_one({'user_id': self.main_user}, {'$set': {'request.' + campo: odr}})
            else:
                self.colection.update_one({'user_id': self.main_user}, {'$set': {'request.' + campo: valor}})

    def laboral(self):
        tz = pytz.timezone('America/Mexico_City')
        ct = datetime.now(tz=tz)
        hour = ct.hour
        weekday = ct.isoweekday()
        if 1 <= weekday <= 6 and 8 <= hour <= 16:
            laboral = True
        else:
            laboral = False
        return laboral

    def saludar(self, users):
        # abril 5  octubre 25
        # tz = pytz.timezone('America/Mexico_City')
        # ct = datetime.now(tz=tz)
        # hour = ct.hour
        # weekday = ct.isoweekday()
        if self.laboral():
            mensaje = "@#AT#@@#TITLE#@¡Hola! 👋 Soy el Asistente Virtual de Almacenes Anfora. 🤖 🍴" \
                      + "\n¿Qué deseas? Escribe el número." \
                      + "@#AT#@@#OPTION#@\n1. Sucursales (Horario, teléfono y ubicación) ☎️" \
                      + "@#AT#@@#OPTION#@\n2. Tienda en línea 🛒" \
                      + "@#AT#@@#OPTION#@\n3. Cotizaciones 💰" \
                      + "@#AT#@@#OPTION#@\n4. Promociones 🔔" \
                      + "@#AT#@@#OPTION#@\n5. Almacenes Anfora: Antes de visitarnos, te invitamos a conocer las medidas preventivas " \
                        "que tenemos actualmente en nuestras tiendas, solo escribe 5" \
                      + "@#AT#@@#OPTION#@\n6. Salir👋 @#AT#@@#IMG#@https://www.broadcasterbot.com/cliente/almacenesanfora/logo.jpg"
        else:
            mensaje = "@#AT#@@#TITLE#@¡Hola! 👋 Soy el Asistente Virtual de Almacenes Anfora. 🤖 🍴" \
                      + "Nuestros horarios de servicio son de Lunes a Sábado de 08:00 am a 05:00 pm." \
                      + "\n¿Qué deseas? Escribe el número." \
                      + "@#AT#@@#OPTION#@\n1. Sucursales (Horario, teléfono y ubicación) ☎️" \
                      + "@#AT#@@#OPTION#@\n2. Tienda en línea 🛒" \
                      + "@#AT#@@#OPTION#@\n3. Cotizaciones 💰" \
                      + "@#AT#@@#OPTION#@\n4. Promociones 🔔" \
                      + "@#AT#@@#OPTION#@\n5. Almacenes Anfora: Antes de visitarnos, te invitamos a conocer las medidas preventivas " \
                        "que tenemos actualmente en nuestras tiendas, solo escribe 5" \
                      + "@#AT#@@#OPTION#@\n6. Salir👋 @#AT#@@#IMG#@https://www.broadcasterbot.com/cliente/almacenesanfora/logo.jpg"
        botones = [{'payload': 'sucursales',
                    'title': 'Sucursales (Horario, teléfono y ubicación)'},
                   {'payload': 'tienda_linea',
                    'title': 'Tienda en línea'},
                   {'payload': 'cotizaciones',
                    'title': 'Cotizaciones'},
                   {'payload': 'promociones',
                    'title': 'Promociones'},
                   {'payload': 'mensaje_covid',
                    'title': 'Almacenes Anfora: Antes de visitarnos, te invitamos a conocer las medidas preventivas '
                             'que tenemos actualmente en nuestras tiendas, solo escribe 5 '},
                   {'payload': 'salir',
                    'title': 'salir'}]
        for i in range(len(botones)):
            botones[i]['number'] = str(i + 1)
            botones[i]['letter number'] = convert_to_letters(i + 1)
        users['buttons'] = botones

        return mensaje, users

    def get_response(self, D, interpreter, agent, users):
        # Se definen las variables del modelo
        # texto
        if D.get('from'):
            self.main_user = D.get('from')
        else:
            self.main_user = D.get('From')
        self.agent = agent
        self.interpreter = interpreter

        if D.get('body'):
            self.original_text = D['body']
        elif D.get('Body'):
            self.original_text = D['Body']
        else:
            self.original_text = 'xxxx'
        # coordenadas
        self.lat = D.get("lat")
        self.lng = D.get("lng")
        if D.get("lat") and D.get("lng"):
            self.original_text = "mapa"
        else:
            lat = ""
            lng = ""
        if D.get("audio"):
            audio = D.get("audio")
            D["body"] = 'xxxx'
        # Se verifica si el usuario existe
        if not users.get(self.main_user):
            users[self.main_user] = {'name': 'Humano', 'buttons': []}
        response, users[self.main_user] = self.bot(self.original_text, users[self.main_user])
        print("ESTO ES RESPONSE")
        print(response)
        response = str(response)
        titles = []
        images = []
        pdfs = []
        xlsxs = []
        flags = []
        options_0 = []
        texts_0 = []
        options = []
        texts = []
        messages = []
        lista = response.split("@#AT#@")
        print("=0" * 30)
        print(lista)
        print("=0" * 30)
        text = ""

        for elem in lista:
            if "@#TITLE#@" in elem:
                title = elem.replace('@#TITLE#@', '')
                titles.append(title)
            elif "@#OPTION_0#@" in elem:
                option = elem.replace('@#OPTION_0#@', '')
                options_0.append(option)
            elif "@#IMG#@" in elem:
                link_image = elem.replace('@#IMG#@', '')
                image = {link_image: None}
                images.append(image)
            elif "@#PDF#@" in elem:
                pdf = elem.replace('@#PDF#@', '')
                pdfs.append(pdf)
            elif "@#XLSX#@" in elem:
                xlsx = elem.replace('@#XLSX#@', '')
                xlsxs.append(xlsx)
            elif "@#CAPTION#@" in elem and images:
                option = elem.replace('@#CAPTION#@', '')
                images[-1][link_image] = option
            elif "@#TEXT_0#@" in elem:
                text = elem.replace('@#TEXT_0#@', '')
                texts_0.append(text)
            elif "@#OPTION#@" in elem:
                option = elem.replace('@#OPTION#@', '')
                options.append(option)
            elif "@#TEXT#@" in elem:
                text = elem.replace('@#TEXT#@', '')
                texts.append(text)
            elif "@#DELEGATE#@" in elem:
                flags.append('@#DELEGATE#@')
            elif "@#COMPLETE#@" in elem:
                flags.append('@#COMPLETE#@')

        text_options = ""

        for title in titles:
            text = text + title
        for option in options:
            text = text + option
        for image in images:
            url = list(image.keys())[0]
            message = {
                "type": "image",
                "url": url.strip()
            }
            messages.append(message)
        for pdf in pdfs:
            message = {
                "type": "pdf",
                "url": pdf
            }
            messages.append(message)
        for xlsx in xlsxs:
            message = {
                "type": "xlsx",
                "url": xlsx
            }
            messages.append(message)
        for image in images:
            caption = list(image.values())[0]
            if caption:
                text = caption + "\n" + text
        ls = []
        for message in messages:
            dic = {"file":
                       message,
                   "text": ""}
            ls.append(dic)
        if text and ls:
            ls[0]['text'] = text.rstrip()
        new_title = ""
        for title in titles:
            new_title = new_title + "" + title
        new_title = new_title.rstrip()
        if images:
            url2 = list(images[0].keys())[0].strip()
        else:
            url2 = ""
        opciones = []

        print("000000")
        print(options)

        # ----
        if options:
            for index, opcion in enumerate(options):
                if index == len(options) - 1:
                    opcion = opcion.rstrip("\n")
                dic = {"description": opcion,
                       "value": index + 1}
                text_options = text_options + ' ' + opcion
                opciones.append(dic)
        optionTypes = ""

        print("llllllssssss")
        print(ls)

        if ls:
            optionTypes = "RICH_CARD"
        else:
            if text_options != "":
                text_options = "\n" + text_options
            ls = [
                {
                    "file": {},
                    "text": new_title.strip() + text_options.rstrip()
                },
            ]

        if not optionTypes and not text_options:
            optionTypes = "TEXT"
            return {"messages": ls,
                    "flags": flags,
                    "messagesOptions": {},
                    "optionTypes": optionTypes}
            if not optionTypes and text_options:
                optionTypes = "SUGGESTIONS"

        if not optionTypes and text_options:
            optionTypes = "SUGGESTIONS"

        return {
            "messages": ls,
            "flags": flags,
            "messagesOptions": {
                "title": new_title.rstrip(),
                "description": new_title.rstrip(),
                "urlImage": url2,
                "options": opciones
            },
            "optionTypes": optionTypes,
            "workGroupId": None
        }
