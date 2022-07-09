import tkinter as tk
from interfaz_01_esqueleto import *


def main():
    root = tk.Tk()
    root.wm_title("Sistema de captura de Recibos UNAM")
    app = Ventana(root)
    app.mainloop()


if __name__ == "__main__":
    main()
