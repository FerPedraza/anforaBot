
def fecha(self):
    hora=datetime.now()
    dias = {
        "Monday":"lunes",
        "Tuesday":"martes",
        "Wednesday":"miércoles",
        "Thursday":"jueves",
        "Friday":"viernes",
        "Saturday":"sábado",
        "Sunday":"domingo"
        }
    meses={
        "January":"Enero",
        "February":"Febrero",
        "March":"Marzo",
        "April":"Abril",
        "May":"Mayo",
        "June":"Junio",
        "July":"Julio",
        "August":"Agosto",
        "September":"Septiembre",
        "October":"Octubre",
        "November":"Noviembre",
        "December":"Diciembre"
            }
    mensaje = 'hoy es '+dias[hora.strftime("%A")] + ' ' + hora.strftime("%d")+' de '+meses[hora.strftime("%B")]+' del '+hora.strftime("%Y") 
    return mensaje

    