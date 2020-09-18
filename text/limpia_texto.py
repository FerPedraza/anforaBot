import re

def clean_text(texto):
    texto=texto.lower()
    texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').strip()
    for i in range(len(texto)):
        if texto[i].isalpha() == False and texto[i].isdigit() == False:
            texto = texto.replace(texto[i],' ') 
    texto = texto.strip()
    if texto.find('@') == -1:
        texto = re.sub("\s\s+" , " ", texto)
    if texto == '':
        return 'xxxxx'
    else:
        return texto

def middle_clean_text(texto):
    texto = texto.lower()
    texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').strip()
    for i in range(len(texto)):
        if texto[i].isalpha() == False and texto[i].isdigit() == False and texto[i] != "-"\
                and texto[i] != "." and texto[i] != "@" and texto[i] != " " and texto[i] != "_":
            texto = texto.replace(texto[i], ' ')
    texto = texto.strip()
    if texto == '':
        return 'xxxxx'
    else:
        return texto

