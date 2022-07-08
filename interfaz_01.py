
import sqlite3
from tkinter import *
from tkinter import ttk



conexion =  sqlite3.connect("BDRecibos")
cursor =  conexion.cursor()

class Aplicacion():
    ventana = 0
    posx_y = 0
        
    def __init__(self):                             
        self.raiz = Tk()
        self.raiz.geometry('600x200+500+50')
        self.raiz.resizable(0,0)
        self.raiz.title("Ventana de aplicación")
        Texto1 = Label(self.raiz, text = "Registro de recibos de pago en la Base de datos")
        Texto1.config(font=("Consolas", 12))
        Texto1.grid(row=0, column=1)

        btn = ttk.Label(self.raiz, text='').grid(row=1, column=0)
                
        botonCaptura = ttk.Button(self.raiz, text='Captura un recibo')
        botonCaptura.grid(row=2, column=0, padx=20, pady=10)

        btn = ttk.Label(self.raiz, text='').grid(row=3, column=0)
        
        boton = ttk.Button(self.raiz, text='Abrir', 
                           command=self.abrir)
        boton.grid(row=4, column=0, padx=20, pady=10)
 
        self.raiz.mainloop()

    def abrir(self):
        ''' Construye una ventana de diálogo '''
        
        self.dialogo = Toplevel()
        Aplicacion.ventana+=1
        Aplicacion.posx_y += 50
        tamypos = '200x100+'+str(Aplicacion.posx_y)+ \
                  '+'+ str(Aplicacion.posx_y)
        self.dialogo.geometry(tamypos)
        self.dialogo.resizable(0,0)
        ident = self.dialogo.winfo_id()
        titulo = str(Aplicacion.ventana)+": "+str(ident)
        self.dialogo.title(titulo)
        boton = ttk.Button(self.dialogo, text='Cerrar', 
                           command=self.dialogo.destroy)   
        boton.pack(side=BOTTOM, padx=20, pady=20)
        
        # Convierte la ventana 'self.dialogo' en 
        # transitoria con respecto a su ventana maestra 
        # 'self.raiz'.
        # Una ventana transitoria siempre se dibuja sobre
        # su maestra y se ocultará cuando la maestra sea
        # minimizada. Si el argumento 'master' es
        # omitido el valor, por defecto, será la ventana
        # madre.
        
        self.dialogo.transient(master=self.raiz)

        # El método grab_set() asegura que no haya eventos 
        # de ratón o teclado que se envíen a otra ventana 
        # diferente a 'self.dialogo'. Se utiliza para 
        # crear una ventana de tipo modal que será 
        # necesario cerrar para poder trabajar con otra
        # diferente. Con ello, también se impide que la 
        # misma ventana se abra varias veces. 
        
        self.dialogo.grab_set()
        self.raiz.wait_window(self.dialogo)

    def defineFecha(fecha):
        '''Función que ajusta el formato de fecha para sqlite3 de "DD/MM/YYYY" al "YYYY/MM/DD" '''
    
        anio = fecha[6:10]
        mes = fecha[3:5]
        dia = fecha[0:2]
        nuevafecha = anio + '-' + mes + '-' + dia
        return nuevafecha


    def datosRecibo(quincena, fecha, monto, qmes):
        '''Función que ingresa un solo recibo a la base de datos,
        ocupando los respectivos campos de quincena, fecha, monto y
        quincena del mes. Se ajusta el formato de fecha que se ingresa:
        "DD/MM/YYYY" al formato para sqlite3: "YYYY-MM-DD" '''

        nuevafecha = defineFecha(fecha)
        cadenaSQL = 'INSERT INTO recibos VALUES (NULL, {0:}, {1:}, {2:}, {3:})'.format(quincena, nuevafecha, monto, qmes)
        
        return cadenaSQL
    
def main():
    mi_app = Aplicacion()
    return(0)

if __name__ == '__main__':
    main()