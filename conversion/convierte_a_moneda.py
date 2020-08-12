
from untitled import numero_a_letras
MONEDA_SINGULAR = 'peso'
MONEDA_PLURAL = 'pesos'

CENTIMOS_SINGULAR = 'centavo'
CENTIMOS_PLURAL = 'centavos'

def convert_to_currency(numero):
    numero_entero = int(numero)
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    centimos = ''
    if parte_decimal == 1:
        centimos = CENTIMOS_SINGULAR
    else:
        centimos = CENTIMOS_PLURAL
    moneda = ''
    if numero_entero == 1:
        moneda = MONEDA_SINGULAR
    else:
        moneda = MONEDA_PLURAL
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('uno', 'un')
    letras_decimal = 'con %s %s' % (numero_a_letras(parte_decimal).replace('uno', 'un'), centimos)
    letras = '%s %s %s' % (letras, moneda, letras_decimal)
    return letras

