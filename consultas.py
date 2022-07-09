import sqlite3


class Consultas:

    def __init__(self):
        self.conexion = sqlite3.connect("BDRecibos")

        self.year = None
        self.mes = None
        self.dia = None
        self.nueva_fecha = None
        self.fecha_modificada = None

    def __str__(self):
        datos = self.consulta_registros()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def define_fecha(self, fecha):
        """Función que ajusta el formato de fecha para sqlite3
        de "DD/MM/YYYY" al "YYYY/MM/DD" """
        print(fecha)
        self.year = fecha[6:10]
        self.mes = fecha[3:5]
        self.dia = fecha[0:2]
        self.nueva_fecha = "'" + self.year + '-' + self.mes + '-' + self.dia + "'"
        return self.nueva_fecha

# TODO Falta revisar la longitud de la cadena, para recuperar el formato inicial de fecha
    def regresa_fecha(self, fecha):
        self.year = fecha[1:5]
        self.mes = fecha[6:8]
        self.dia = fecha[9:11]
        self.fecha_modificada = self.dia + '-' + self.mes + '-' + self.year
        return self.fecha_modificada

    def consulta_registros(self):
        cur = self.conexion.cursor()
        cur.execute("SELECT * from recibos ORDER BY fecha")
        datos = cur.fetchall()
        cur.close()
        return datos

    def agrega_recibo(self, quincena, fecha, monto, num_quincena):
        """Función que ingresa un solo recibo a la base de datos,
            ocupando los respectivos campos de quincena, fecha, monto y
            quincena del mes. Se ajusta el formato de fecha que se ingresa:
            "DD/MM/YYYY" al formato para sqlite3: "YYYY/MM/DD" """

        cur = self.conexion.cursor()
        nueva_fecha = self.define_fecha(fecha)

        cadena_sql = 'INSERT INTO recibos VALUES (NULL, {0:}, {1:}, {2:}, {3:})'.format(quincena, nueva_fecha, monto,
                                                                                        num_quincena)
        cur.execute(cadena_sql)
        self.conexion.commit()
        # self.fetch_data()
        cur.close()

    def elimina_recibo(self, clave: object) -> object:
        cur = self.conexion.cursor()
        cadena_sql = 'DELETE FROM recibos WHERE ID = {0:}'.format(clave)
        cur.execute(cadena_sql)
        n = cur.rowcount
        self.conexion.commit()
        cur.close
        return n

    def actualiza_datos(self, clave, quincena, fecha, monto, numquincena):
        cur = self.conexion.cursor()
        cadena2_sql = 'UPDATE recibos SET quincena={0:}, fecha={1:}, monto={2:}, qmes={3:} WHERE id={4:}'.format(
            quincena, fecha, monto, numquincena, clave)
        print(cadena2_sql)
        cur.execute(cadena2_sql)
        n = cur.rowcount
        self.conexion.commit()
        cur.close()


    # def fetch_data(self):
    #     conexion = sqlite3.connect("BDRecibos")
    #     cursor = conexion.cursor()
    #     cursor.execute('SELECT id, quincena, fecha, monto, qmes FROM recibos ORDER BY fecha ASC')
    #     rows = cursor.fetchall()
    #     if len(rows) != 0:
    #         for row in rows:
    #             self.recibo_tabla.insert('', END, values=row)
    #
    #
    #
    #
    #
    #
