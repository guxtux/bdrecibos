# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:05:54 2020

@author: gusto
"""
from tkinter import *
from tkinter import ttk
# from tkinter import messagebox
import sqlite3


class Ventana:

    def __init__(self, ventana_01):

        self.ventana = ventana_01
        self.ventana.title("Sistema de registro de recibos de pago UNAM")
        self.ventana.geometry("600x600+100+100")

        title = Label(self.ventana, text="Registro de recibos de pago en la Base de datos",
                      font=("Consolas", 20, "bold"))
        title.pack(side=TOP)

        # ------Variables------
        self.id_var = IntVar()
        self.fecha_var = StringVar()
        self.quincena_var = IntVar()
        self.numquincena_var = IntVar()
        self.monto_var = DoubleVar()

        manage_frame = Frame(self.ventana, bd=4, bg="#a3d1f0")
        manage_frame.place(x=30, y=50, width=550, height=220)

        manage_title = Label(manage_frame, text="Captura de registro de recibo", font=("Consolas", 14, "bold"),
                             bg="#a3d1f0")
        manage_title.pack(side=TOP)

        label_fecha = Label(manage_frame, text="Fecha", bg="#a3d1f0")
        label_fecha.place(x=10, y=40)

        text_fecha = Entry(manage_frame, width=15, textvariable=self.fecha_var)
        text_fecha.place(x=120, y=40)

        label_quincena = Label(manage_frame, text="Quincena", bg="#a3d1f0")
        label_quincena.place(x=10, y=80)

        valores = []
        for i in range(1, 25):
            valores.append(i)

        combo_eligequincena = ttk.Combobox(manage_frame, textvariable=self.quincena_var, width=10, state='readonly')
        combo_eligequincena['values'] = valores
        combo_eligequincena.set(valores[0])
        combo_eligequincena.place(x=120, y=80)

        label_pagoquincena = Label(manage_frame, text="Pago quincena",
                                   bg="#a3d1f0")
        label_pagoquincena.place(x=10, y=120)

        numvalores = [1, 2, 3]

        combo_numquincena = ttk.Combobox(manage_frame, textvariable=self.numquincena_var, width=15, state='readonly')
        combo_numquincena['values'] = numvalores
        combo_numquincena.set(numvalores[0])
        combo_numquincena.place(x=120, y=120)

        label_monto = Label(manage_frame, text="Monto", bg="#a3d1f0")
        label_monto.place(x=10, y=160)

        text_monto = Entry(manage_frame, width=15, textvariable=self.monto_var)
        text_monto.place(x=120, y=160)

        botones_frame = Frame(manage_frame, bg="#f0f838")
        botones_frame.place(x=350, y=40, width=150, height=172)

        boton_agregar = Button(botones_frame, bd=4, text="Agregar", width=13, height=2, command=self.agrega_recibo)
        boton_agregar.place(x=10, y=10)

        boton_actualizar = Button(botones_frame, bd=4, text="Actualizar", width=13, height=2,
                                  command=self.actualiza_datos)
        boton_actualizar.place(x=10, y=50)

        boton_eliminar = Button(botones_frame, bd=4, text="Eliminar", width=13, height=2)
        boton_eliminar.place(x=10, y=90)

        boton_limpiar = Button(botones_frame, bd=4, text="Limpiar", width=13, height=2, command=self.limpiar)
        boton_limpiar.place(x=10, y=130)

        detalle_frame = Frame(self.ventana, bd=4, bg="#f0b7a3")
        detalle_frame.place(x=30, y=275, width=550, height=300)

        # label_busqueda = Label(detalle_frame, text="Búsqueda por Año: ", bg="#f0b7a3")
        # label_busqueda.place(x=10, y=20)

        # busqueda = StringVar()
        # busqueda.set('Año')
        # numopciones = ['Año', 'Quincena']

        # option_busqueda = OptionMenu(detalle_frame, busqueda, *numopciones)
        # option_busqueda.config(width=10)
        # option_busqueda.place(x=90, y=20)
        #
        # boton_buscar = Button(detalle_frame, text="Buscar", width=7, height=2)
        # boton_buscar.place(x=230, y=15)

        tabla_frame = Frame(detalle_frame, bd=4, bg="#e5c377")
        tabla_frame.place(x=10, y=60, width=520, height=200)

        scroll_x = Scrollbar(tabla_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(tabla_frame, orient=VERTICAL)

        self.recibo_tabla = ttk.Treeview(tabla_frame, columns=("ID", "Quincena", "Fecha", "Monto", "Pago quincena"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.recibo_tabla.xview)
        scroll_y.config(command=self.recibo_tabla.yview)

        self.recibo_tabla.heading("ID", text="ID")
        self.recibo_tabla.heading("Quincena", text="Quincena")
        self.recibo_tabla.heading("Fecha", text="Fecha")
        self.recibo_tabla.heading("Monto", text="Monto")
        self.recibo_tabla.heading("Pago quincena", text="Pago quincena")

        self.recibo_tabla['show'] = 'headings'

        self.recibo_tabla.column("ID", width=50)
        self.recibo_tabla.column("Quincena", width=100)
        self.recibo_tabla.column("Fecha", width=100)
        self.recibo_tabla.column("Monto", width=100)
        self.recibo_tabla.column("Pago quincena", width=100)

        self.recibo_tabla.bind("<ButtonRelease-1>", self.obtiene_cursor)
        self.fetch_data()

        self.recibo_tabla.pack(fill=BOTH, expand=1)

    def agrega_recibo(self):
        """Función que ingresa un solo recibo a la base de datos,
            ocupando los respectivos campos de quincena, fecha, monto y
            quincena del mes. Se ajusta el formato de fecha que se ingresa:
            "DD/MM/YYYY" al formato para sqlite3: "YYYY/MM/DD" """

        def define_fecha(fecha):
            """Función que ajusta el formato de fecha para sqlite3
            de "DD/MM/YYYY" al "YYYY/MM/DD" """

            year = fecha[6:10]
            mes = fecha[3:5]
            dia = fecha[0:2]
            nueva_fecha = "'" + year + '-' + mes + '-' + dia + "'"
            return nueva_fecha

        conexion = sqlite3.connect("BDRecibos")
        cursor = conexion.cursor()
        ajuste_fecha = define_fecha(self.fecha_var.get())

        cadena_sql = 'INSERT INTO recibos VALUES (NULL, {0:}, {1:}, {2:}, {3:})'.format(self.quincena_var.get(),
                                                                                        ajuste_fecha,
                                                                                        self.monto_var.get(),
                                                                                        self.numquincena_var.get())
        cursor.execute(cadena_sql)
        conexion.commit()
        self.fetch_data()
        self.limpiar()
        conexion.close()

    def fetch_data(self):
        conexion = sqlite3.connect("BDRecibos")
        cursor = conexion.cursor()
        cursor.execute('SELECT id, quincena, fecha, monto, qmes FROM recibos ORDER BY fecha ASC')
        rows = cursor.fetchall()
        if len(rows) != 0:
            for row in rows:
                self.recibo_tabla.insert('', END, values=row)

    def limpiar(self):
        self.fecha_var.set('')
        self.monto_var.set('')
        self.quincena_var.set('1')
        self.numquincena_var.set('1')

    def obtiene_cursor(self):
        cursor_row = self.recibo_tabla.focus()
        contenido = self.recibo_tabla.item(cursor_row)
        row = contenido['values']
        print(row)
        self.id_var.set(row[0])
        self.quincena_var.set(row[1])
        self.fecha_var.set(row[2])
        self.monto_var.set(row[3])
        self.numquincena_var.set(row[4])

    def actualiza_datos(self):
        conexion = sqlite3.connect("BDRecibos")
        cursor = conexion.cursor()
        cadena2_sql = 'UPDATE recibos SET quincena={0:}, fecha={1:}, monto={2:}, qmes={3:} WHERE id={4:}'.format(
            self.quincena_var.get, self.fecha_var.get(), self.monto_var.get, self.numquincena_var.get(),
            self.id_var.get())

        cursor.execute(cadena2_sql)
        conexion.commit()
        self.fetch_data()
        self.limpiar()
        conexion.close()


ventana = Tk()
ob = Ventana(ventana)
ventana.mainloop()
