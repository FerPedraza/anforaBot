from conversion.convierte_a_letras import convert_to_letters

def yes_or_not(payloadSi,payloadNo,menu,title):
    botones=[{'payload':payloadSi,'title':'Si'},{'payload':payloadNo,'title':'No'}]
    if menu != None:
        botones.append({'payload':menu,'title':title})
    for i in range(len(botones)):
        botones[i]['number'] = str(i + 1)
        botones[i]['letter number'] = convert_to_letters(i+1)
    return botones

def only_one_button(title,menu):
    botones=[{'payload':menu,'title':title}]
    for i in range(len(botones)):
        botones[i]['number'] = str(i + 1)
        botones[i]['letter number'] = convert_to_letters(i+1)
    return botones