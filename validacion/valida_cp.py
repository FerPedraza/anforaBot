
def valida_cp(cp):
    with open('./validacion/data/CPdescarga.txt',encoding='latin-1') as f:
        cps = f.readlines()
        for i in cps:
            if i.find(cp) == 0:
                lista = i.split("|")
                asentamiento = lista[1]
                municipio = lista[3]
                estado = lista[4]
                ciudad = lista[5]
                return asentamiento, municipio, ciudad, estado
                break
        else:
            return -1


