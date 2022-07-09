def define_fecha(fecha):
    """Función que ajusta el formato de fecha para sqlite3
    de "DD/MM/YYYY" al "YYYY/MM/DD" """
    print(fecha)
    year = fecha[6:10]
    mes = fecha[3:5]
    dia = fecha[0:2]
    nueva_fecha = "'" + year + '-' + mes + '-' + dia + "'"
    return nueva_fecha


def regresa_fecha(fecha):
    print(fecha)
    year = fecha[1:5]
    mes = fecha[6:8]
    dia = fecha[9:11]
    fecha_modificada = dia + '-' + mes + '-' + year
    print(year)
    print(mes)
    print(dia)
    return fecha_modificada


a = define_fecha("23/07/2019")

print(a)

b = regresa_fecha(a)
print(b)