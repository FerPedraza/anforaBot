from subprocess import call
from os import listdir
def unpacking_tar():
    list = listdir("./models")
    number_tar = 0
    list_tar = []
    for i in list:
        if i.find(".tar.gz") != -1:
            number_tar = number_tar + 1
            list_tar.append(i[:8] + i[9:15])
            list_tar.append("20200814150840")
            list_tar = sorted(list_tar)
            last_tar = list_tar[0][:8] + "-" + list_tar[0][8:]+ ".tar.gz"
            for i in list_tar:
                if i != last_tar:
                    call(f"rm {}")
#    call("")

unpacking_tar()