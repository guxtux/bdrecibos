# -*- coding: utf-8 -*-
"""
Created on Thu Jul 1 18:34 2022

@author: gustavo
"""
import tkinter as tk
# from tkinter import ttk


class Aplicacion:

    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de registro de recibos de pago UNAM")
        self.master.geometry('400x250')

        self.inicializar_gui()

    def inicializar_gui(self):

        manage_frame = tk.Frame(self.master, width=399, height=249)
        # manage_frame.place(x=0, y=0, width=399, height=249)
        manage_frame.pack(fill=tk.BOTH, expand=1)
        manage_frame.config(bd=4, bg="#a3d1f0")

        btn_registro = tk.Button(manage_frame, text='Registra Recibo', font=('Consolas', 24))
        # btn_registro.place(x=100, y=50)
        btn_registro.pack(fill=tk.BOTH, expand=1, padx=30, pady=10)

        btn_consulta = tk.Button(manage_frame, text='Consulta', font=('Consolas', 24))
        # btn_consulta.place(x=100, y=100)
        btn_consulta.pack(fill=tk.BOTH, expand=1, padx=30, pady=10)

        btn_salir = tk.Button(manage_frame, text='Salir', font=('Consolas', 24), command=self.master.destroy)
        # btn_salir.place(x=100, y=150)
        btn_salir.pack(fill=tk.BOTH, expand=1, padx=30, pady=10)


def main():
    root = tk.Tk()
    Aplicacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
