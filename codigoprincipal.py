import sqlite3

conexion = sqlite3.connect("BDRecibos")
cursor = conexion.cursor()


# instruccion_sql = "CREATE TABLE recibos (id INTEGER PRIMARY KEY AUTOINCREMENT, quincena INT, \
#                                     fecha VARCHAR(10), monto REAL, qmes INT)"
# cursor.execute(instruccion_sql)


def define_fecha(fecha):
    """Función que ajusta el formato de fecha para sqlite3
    de "DD/MM/YYYY" al "YYYY/MM/DD" """

    anio = fecha[6:10]
    mes = fecha[3:5]
    dia = fecha[0:2]
    nueva_fecha = anio + '/' + mes + '/' + dia
    return nueva_fecha


def datos_recibo(quincena, fecha, monto, qmes):
    """Función que ingresa un solo recibo a la base de datos,
    ocupando los respectivos campos de quincena, fecha, monto y
    quincena del mes. Se ajusta el formato de fecha que se ingresa:
    "DD/MM/YYYY" al formato para sqlite3: "YYYY/MM/DD" """

    nueva_fecha = define_fecha(fecha)
    cadena_sql = 'INSERT INTO recibos VALUES (NULL, {0:}, {1:}, {2:}, {3:})'.format(quincena, nueva_fecha, monto,
                                                                                    qmes)

    return cadena_sql


# --------------------------------------------
# Secuencia para ingresar un solo recibo a la BD
# insertaSQL = datosRecibo(7, '02/04/2020', 1649.45, 1)
# cursor.execute(insertaSQL)
# --------------------------------------------


def genera_lista(veces):
    """Función que genera una lista de tuplas con los valores de los campos
    para los recibos que se van a ingresar en la BD """
    lista1 = []

    for i in range(veces):
        lista2 = []
        print('\nRegistro ' + str(i + 1) + ' \n')
        quincena = int(input('Quincena : '))
        fecha = str(input('Fecha de cobro : '))
        monto = float(input('Monto : '))
        qmes = int(input('Quincena mes: '))
        lista2.append(quincena)
        lista2.append(define_fecha(fecha))
        lista2.append(monto)
        lista2.append(qmes)
        tupla = tuple(lista2)
        lista1.append(tupla)

    print(lista1)
    return lista1


# -----------------------------------------------------------
# Secuencia para elaborar la lista con los campos de registros
# n_recibos = int(input('Número de recibos a ingresar a la BD: '))
# lista = generaLista(n_recibos)

# cursor.executemany("INSERT INTO recibos VALUES (NULL, ?, ?, ?, ?)", lista)
# -----------------------------------------------------------

# conexion.commit()
# print('Se ingresaron debidamente los registros a la BD')

# ---------------------------------------------------
# Consulta para recuperar todos los registros de la BD
# No utiliza el conexion.commit()


cursor.execute("SELECT * FROM recibos")
contenido = cursor.fetchall()

for elemento in contenido:
    print(elemento)
# ---------------------------------------------------

# Consulta para recuperar la suma del campo monto
cursor.execute("SELECT SUM(monto) FROM recibos")
suma_monto = cursor.fetchall()
valor_suma = str(suma_monto[0]).strip("(").strip(",)")
print("La suma del monto obtenido es: ${0:.2f}".format(float(valor_suma)))

conexion.close()
