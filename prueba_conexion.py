import mysql.connector

cnn = mysql.connector.connect(host="localhost", user="root", password="", database="BDRecibos")

cur = cnn.cursor()
cur.execute('SELECT * FROM recibos WHERE YEAR(fecha) = 2022')
datos = cur.fetchall()
cur.close()
cnn.close()

for linea in datos:
    print(linea)
