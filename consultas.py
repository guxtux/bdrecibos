import datetime
import mysql.connector


class Consultas:

    def __init__(self):

        self.conexion = mysql.connector.connect(host="localhost", user="root", password="admingus_$2024",
                                                database="BDRecibos")

        self.year = None
        self.mes = None
        self.dia = None
        self.nueva_fecha = None
        self.nueva_fecha_02 = None
        self.fecha_sin = None

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
        self.nueva_fecha = "'" + self.year + "-" + self.mes + "-" + self.dia + "'"
        return self.nueva_fecha

    def regresa_fecha(self, fecha):
        self.year = fecha[0:4]
        self.mes = fecha[5:7]
        self.dia = fecha[8:10]
        self.nueva_fecha_02 = "'" + self.dia + "-" + self.mes + "-" + self.year + "'"
        return self.nueva_fecha_02

    def quita_comillas(self, fecha_sin):
        self.year = fecha_sin[0:4]
        self.mes = fecha_sin[5:7]
        self.dia = fecha_sin[8:10]
        print(self.year, self.mes, self.dia)
        self.fecha_sin = self.dia + "-" + self.mes + "-" + self.year
        print(self.fecha_sin)
        return self.fecha_sin

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
        print(nueva_fecha, type(nueva_fecha))

        cadena_sql = 'INSERT INTO recibos VALUES (NULL, {0:}, {1:}, {2:}, {3:})'.format(quincena, nueva_fecha, monto,
                                                                                        num_quincena)
        cur.execute(cadena_sql)
        self.conexion.commit()
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
        cur.execute(cadena2_sql)
        n = cur.rowcount
        self.conexion.commit()
        cur.close()
