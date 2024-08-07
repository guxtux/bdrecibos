import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from consultas import *


class Ventana(tk.Frame):
    cadena_consulta = Consultas()

    def __init__(self, master=None):
        super().__init__(master, width=600, height=475)

        self.texto_fecha = None
        self.combo_quincena = None
        self.combo_pago_quincena = None
        self.texto_monto = None
        self.id = -1
        self.fecha_sin_comillas = None

        self.fecha_var = None
        self.quincena_var = None
        self.numquincena_var = None
        self.monto_var = None

        self.boton_nuevo = None
        self.boton_guardar = None
        self.boton_actualizar = None
        self.boton_eliminar = None
        self.boton_limpiar = None
        self.boton_cancelar = None
        self.grid_recibo = None
        self.boton_salir = None

        self.master = master
        self.pack()
        self.inicializar_gui()
        self.cargar_recibo()
        self.habilitar_cajas("disabled")
        self.habilitar_botones("disabled")

    def limpiar(self):
        self.texto_fecha.delete(0, tk.END)
        self.texto_monto.delete(0, tk.END)
        self.combo_quincena.set('1')
        self.combo_pago_quincena.set('1')

    def limpia_grid(self):
        for item in self.grid_recibo.get_children():
            self.grid_recibo.delete(item)

    def nuevo_registro(self):
        self.habilitar_cajas("normal")
        self.boton_actualizar['state'] = "disabled"
        self.boton_limpiar['state'] = "normal"
        self.boton_guardar['state'] = "normal"
        self.boton_nuevo['state'] = "disabled"

    def cargar_recibo(self):
        datos = self.cadena_consulta.consulta_registros()
        for row in datos:
            self.grid_recibo.insert("", tk.END, text=row[0], values=(row[1], row[2], row[3], row[4]))
        if len(self.grid_recibo.get_children()) > 0:
            self.grid_recibo.selection_set(self.grid_recibo.get_children()[-1])

    def guardar_recibo(self):
        if self.id == -1:
            self.cadena_consulta.agrega_recibo(self.combo_quincena.get(), self.texto_fecha.get(),
                                               self.texto_monto.get(),
                                               self.combo_pago_quincena.get())
            messagebox.showinfo("Guardando registro", "Se ha guardado correctamente el registro")
            self.limpiar_cajas()
        else:
            self.cadena_consulta.actualiza_datos(self.id, self.combo_quincena.get(),
                                                 self.cadena_consulta.define_fecha(self.texto_fecha.get()),
                                                 self.texto_monto.get(), self.combo_pago_quincena.get())
            self.id = -1
            messagebox.showinfo("Actualizando registro", "Se ha actualizado el registro correctamente")
            self.limpiar_cajas()

        self.limpia_grid()
        self.cargar_recibo()

    def actualizar_recibo(self):

        selected = self.grid_recibo.focus()
        clave = self.grid_recibo.item(selected, 'text')

        self.habilitar_cajas("normal")
        self.boton_nuevo['state'] = "disabled"
        self.boton_guardar['state'] = "normal"
        self.boton_eliminar['state'] = "normal"

        if clave == '':
            messagebox.showwarning("Modificando registro", "Debes de seleccionar un registro")
        else:
            self.limpiar_cajas()
            self.id = clave
            valores = self.grid_recibo.item(selected, 'values')
            self.texto_fecha.insert(0, self.cadena_consulta.quita_comillas(valores[1]))
            self.combo_quincena.set(valores[0])
            self.texto_monto.insert(0, valores[2])
            self.combo_pago_quincena.set(valores[3])

    def eliminar_recibo(self):

        selected = self.grid_recibo.focus()
        clave = self.grid_recibo.item(selected, 'text')

        if clave == '':
            messagebox.showwarning("Eliminando registro", "Debes de seleccionar un registro")
        else:
            valores = self.grid_recibo.item(selected, 'values')
            data = str(clave) + ', ' + valores[0] + ', ' + valores[1]
            r = messagebox.askquestion('Eliminando registro', 'Deseas eliminar el registro?\n' + data)

            if r == messagebox.YES:
                n = self.cadena_consulta.elimina_recibo(clave)
                if n == 1:
                    messagebox.showinfo('Eliminando registro', 'Elemento eliminado de manera correcta')
                    self.limpia_grid()
                    self.cargar_recibo()
                else:
                    messagebox.showwarning('Eliminando registro', 'No se eliminó el registro')

            self.limpiar_cajas()

        self.habilitar_cajas("disabled")
        self.boton_nuevo['state'] = "normal"
        self.boton_guardar['state'] = "disabled"
        self.boton_eliminar['state'] = "disabled"

    def limpiar_cajas(self):
        self.limpiar()
        self.texto_fecha.focus()

    # falta un botón nuevo registro para que desbloquee las cajas y habilite los botones
    def habilitar_cajas(self, estado):
        self.texto_fecha.configure(state=estado)
        self.texto_monto.configure(state=estado)
        self.combo_quincena.configure(state=estado)
        self.combo_pago_quincena.configure(state=estado)

    def habilitar_botones(self, estado):
        self.boton_guardar.configure(state=estado)
        self.boton_limpiar.configure(state=estado)
        self.boton_eliminar.configure(state=estado)

    def cancela_tarea(self):
        self.habilitar_cajas("disabled")
        self.habilitar_botones("disabled")
        self.boton_actualizar['state'] = "normal"
        self.boton_nuevo['state'] = "normal"

    def obtiene_cursor(self):
        selected = self.grid_recibo.focus()
        print(selected)
        contenido = self.grid_recibo.item(selected)
        print(contenido)

        # row = contenido['values']
        # print(row)
        # self.id_var.set(row[0])
        # self.quincena_var.set(row[1])
        # self.fecha_var.set(row[2])
        # self.monto_var.set(row[3])
        # self.numquincena_var.set(row[4])

    def cerrar_gui(self):
        self.quit()

    def inicializar_gui(self):

        frame_01 = tk.Frame(self, bd=4, bg="#a3d1f0", width=300, height=220)
        frame_01.place(x=0, y=0)

        label_fecha = tk.Label(frame_01, text="Fecha", bg="#a3d1f0")
        label_fecha.place(x=15, y=15)

        self.fecha_var = tk.StringVar()
        self.texto_fecha = tk.Entry(frame_01, width=15, textvariable=self.fecha_var)
        self.texto_fecha.place(x=120, y=15)

        label_quincena = tk.Label(frame_01, text="Quincena", bg="#a3d1f0")
        label_quincena.place(x=15, y=60)

        valores = []
        for i in range(1, 25):
            valores.append(i)

        self.combo_quincena = ttk.Combobox(frame_01, textvariable=self.quincena_var, width=14, state='readonly',
                                           values=valores)
        self.combo_quincena.place(x=120, y=60)
        self.combo_quincena.set(valores[0])

        label_pago_quincena = tk.Label(frame_01, text="Pago quincena", bg="#a3d1f0")
        label_pago_quincena.place(x=15, y=105)

        numvalores = [1, 2, 3]

        self.combo_pago_quincena = ttk.Combobox(frame_01, textvariable=self.numquincena_var, width=14, state='readonly',
                                                values=numvalores)
        self.combo_pago_quincena.place(x=120, y=105)
        self.combo_pago_quincena.set(numvalores[0])

        label_monto = tk.Label(frame_01, text="Monto", bg="#a3d1f0")
        label_monto.place(x=15, y=150)

        self.texto_monto = ttk.Entry(frame_01, width=15, textvariable=self.monto_var)
        self.texto_monto.place(x=120, y=150)

        frame_02 = tk.Frame(self, bd=4, bg="#f0f838", width=300, height=220)
        frame_02.place(x=300, y=0)

        self.boton_nuevo = tk.Button(frame_02, bd=4, text="Nuevo", width=13, height=2, bg="aquamarine",
                                     activebackground="green", activeforeground="white", command=self.nuevo_registro)
        self.boton_nuevo.place(x=40, y=5)

        self.boton_guardar = tk.Button(frame_02, bd=4, text="Guardar", width=13, height=2, bg="dark orange",
                                       activebackground="green", activeforeground="white", command=self.guardar_recibo)
        self.boton_guardar.place(x=40, y=55)

        self.boton_actualizar = tk.Button(frame_02, bd=4, text="Actualizar", width=13, height=2,
                                          bg="maroon1", activebackground="green", activeforeground="white",
                                          command=self.actualizar_recibo)
        self.boton_actualizar.place(x=40, y=105)

        self.boton_eliminar = tk.Button(frame_02, bd=4, text="Eliminar", width=13, height=2, bg="firebrick1",
                                        activebackground="green", activeforeground="white",
                                        command=self.eliminar_recibo)
        self.boton_eliminar.place(x=160, y=5)

        self.boton_limpiar = tk.Button(frame_02, bd=4, text="Limpiar", width=13, height=2, bg="orchid1",
                                       activebackground="green", activeforeground="white", command=self.limpiar_cajas)
        self.boton_limpiar.place(x=160, y=55)

        self.boton_cancelar = tk.Button(frame_02, bd=4, text="Cancelar", width=13, height=2, bg="salmon2",
                                        activebackground="green", activeforeground="white",
                                        command=self.cancela_tarea)
        self.boton_cancelar.place(x=160, y=105)

        self.boton_salir = tk.Button(frame_02, bd=4, text="Salir", width=13, height=2, bg="tomato",
                                     activebackground="green", activeforeground="white", command=self.cerrar_gui)
        self.boton_salir.place(x=160, y=155)

        frame_03 = tk.Frame(self, bd=4, bg="DarkOliveGreen1", width=600, height=100)
        frame_03.place(x=0, y=220)

        self.grid_recibo = ttk.Treeview(frame_03, columns=("Quincena", "Fecha", "Monto", "Pago quincena"))
        # self.grid_recibo.place(x=50, y=5, width=500, height=250)
        self.grid_recibo.pack(side=tk.LEFT)

        self.grid_recibo.column("#0", width=50)
        self.grid_recibo.column("Quincena", width=100, anchor=tk.CENTER)
        self.grid_recibo.column("Fecha", width=100, anchor=tk.CENTER)
        self.grid_recibo.column("Monto", width=100, anchor=tk.CENTER)
        self.grid_recibo.column("Pago quincena", width=100, anchor=tk.CENTER)

        self.grid_recibo.heading("#0", text="ID", anchor=tk.CENTER)
        self.grid_recibo.heading("Quincena", text="Quincena", anchor=tk.CENTER)
        self.grid_recibo.heading("Fecha", text="Fecha", anchor=tk.CENTER)
        self.grid_recibo.heading("Monto", text="Monto", anchor=tk.CENTER)
        self.grid_recibo.heading("Pago quincena", text="Pago quincena", anchor=tk.CENTER)

        self.grid_recibo['selectmode'] = 'browse'

        sb = ttk.Scrollbar(frame_03, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.grid_recibo.config(yscrollcommand=sb.set)
        sb.config(command=self.grid_recibo.yview)

