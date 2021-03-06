from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

import mysql.connector # Importo el conector de MySQL (antes se lo descargó con pip install mysql-connector)
              
class MainWindow: # Clase principal contenedora de todos las funciones del programa.
    def __init__(self, root): # Constructor de la clase.
        # Creacion y Grindeado de los Frames
        self.fondo = 'seashell3'
        self.Frame1 = Frame(root, bg = self.fondo)
        self.Frame1.grid(row = 0, column = 0, pady = 10)
        self.Frame2 = LabelFrame(root, text = 'Lista de cargados', bg = self.fondo)
        self.Frame2.grid(row = 1, column = 0, columnspan = 2)
        self.Frame3 = Frame(root, bg = self.fondo)
        self.Frame3.grid(row = 0, column = 1)
        self.Frame4 = Frame(root, bg = self.fondo)
        self.Frame4.grid(row = 2, column = 0, columnspan = 2)
        
        
        # Declaracion de los Entrys
        self.entrada1, self.entrada2, self.entrada3 = StringVar(), StringVar(), StringVar()
                
        # Funciones armado de ventana.
        def labels(texto, fila, columna):
            label = Label(self.Frame1, text = texto, bg = self.fondo)
            label.grid(row = fila, column = columna)

        def entradas(variable, fila, columna):
            entry = Entry(self.Frame1, textvariable = variable)
            entry.grid(row = fila, column = columna)
            return entry
        
        # Pasaje de valores para Funciones
        labels('Titulo', 0, 0)
        labels('Ruta', 1, 0)
        labels('Descripcion', 2, 0)
                
        self.entry1 = entradas(self.entrada1, 0, 1)
        self.entry2 = entradas(self.entrada2, 1, 1)
        self.entry3 = entradas(self.entrada3, 2, 1)
        self.entry1.focus() # Cuando inicia el programa el cursor se posiciona en este entry.
        
        
        # BOTONES
        botonAgregar = Button(self.Frame1, text = 'Guardar Datos', command = self.agregaraDB) # Boton para grabar datos en BD
        botonAgregar.grid(row = 3, column = 1, pady = 5)

        botonCrearBD = Button(self.Frame3, text = 'Crear BD', command = self.crearBase) # Boton para crear Base si no existe
        botonCrearBD.grid(row = 0, column = 0, padx = 5)

        botonCrearTabla = Button(self.Frame3, text = 'Crear Tabla', command = self.crearTB) # Boton para crear Tabla si no existe.
        botonCrearTabla.grid(row = 0, column = 1)

        botonModificarDato = Button(self.Frame4, text = 'Modificar Entrada', command = self.modificarDato)
        botonModificarDato.grid(row = 0, column = 0, pady = 10)

        botonEliminarDato = Button(self.Frame4, text = 'Eliminar Entrada', command = self.eliminarDato)
        botonEliminarDato.grid(row = 0, column = 1)

        # Mensaje
        self.mensaje = Label(self.Frame4, text = '', bg = self.fondo, fg = 'blue', font = ('15')) # Label que muestra mensaje de accion.
        self.mensaje.grid(row = 1, column = 0, columnspan = 2, sticky = W + E, pady = 5)

        # Creacion del Treeview
        self.resumen = ttk.Treeview(self.Frame2, columns = ('#1', '#2', '#3'))

        # Funciones para armar Treeview
        def treeviewColumn(treeview, nombre, ancho, minimo):
            treeview.column(nombre, width = ancho, minwidth = minimo)
        def treeviewHeading(treeview, nombre, texto):
            treeview.heading(nombre, text = texto)
        
        treeviewColumn(self.resumen, '#0', 40, 20)
        treeviewColumn(self.resumen, '#1', 130, 100)
        treeviewColumn(self.resumen, '#2', 130, 100)
        treeviewColumn(self.resumen, '#3', 130, 100)

        treeviewHeading(self.resumen, '#0', 'ID')
        treeviewHeading(self.resumen, '#1', 'Titulo')
        treeviewHeading(self.resumen, '#2', 'Ruta')
        treeviewHeading(self.resumen, '#3', 'Descripcion')

        self.resumen.grid(row = 0, column = 0)

        # Declaracion del Scrollbar
        scrollb = ttk.Scrollbar(self.Frame2)
        scrollb.grid(row = 0, column = 1, sticky = 'NS')
        
        self.hacerConsulta()
        
    def crearBase(self): # Metodo para crear Base de datos en caso de que mi_plantilla2 no exista.
        while True:
            try:
                mibase = mysql.connector.connect(
                    host ='localhost',
                    user = 'root',
                    passwd = ''
                )
                micursor = mibase.cursor()
                micursor.execute('CREATE DATABASE mi_plantilla2')
                print('Base de datos creada con Exito')
                break
            except mysql.connector.errors.DatabaseError: # En la excepcion pongo el error de base de datos ya creada.
                self.mensaje['text'] = 'La Base de Datos ya está creada.'
                break
            
    def crearTB(self): # Metodo para crear tabla en caso de que producto no exista.
        while True:
            try:
                mibase = mysql.connector.connect(
                    host ='localhost',
                    user = 'root',
                    passwd = '',
                    database="mi_plantilla2"
                )
                micursor = mibase.cursor()
                micursor.execute("CREATE TABLE producto( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, ruta varchar(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion text COLLATE utf8_spanish2_ci NOT NULL )")
                print('Lista creada con Exito')
                break
            except mysql.connector.errors.ProgrammingError: # En la excepcion pongo el error de lista ya creada.
                self.mensaje['text'] = 'La tabla ya está creada.'
                break    
            
    def agregaraDB(self): # Metodo para agregar valores a la tabla desde los Entrys.
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="mi_plantilla2"
        )
        micursor = mibase.cursor()

        if self.entry1.get() == "" and self.entry2.get() == "" and self.entry3.get() == "": # Comprueba si hay campos sin completar
             print ("No cargaste ningun dato")                                              # y muestra un mensaje de error.
             showerror ("Error", "No cargaste ningun dato")
        elif self.entry1.get() == "" or self.entry2.get() == "" or self.entry3.get() == "" :
                print ("Datos incompletos")
                showerror ("Error", " Campos incompletos")
        else:
                print ("\n Nueva alta de datos")
                print ("\n Nombre:", self.entry1.get(),"\n Apellido:", self.entry1.get(), "\n e-mail:", self.entry1.get())
                
                datos = self.entrada1.get(), self.entrada2.get(), self.entrada3.get()
                sql = 'INSERT INTO producto (titulo, ruta, descripcion) VALUES (%s, %s, %s)'
                micursor.execute(sql, datos)
                mibase.commit()
                print(micursor.rowcount, "Cantidad de registros agregados.")
                
                self.entry1.delete(0, END)
                self.entry2.delete(0, END)
                self.entry3.delete(0, END)
                
                self.hacerConsulta()
                self.mensaje['text'] = 'Registro Agregado'
                self.entry1.focus() # Cuando se agregan los datos vuelve al primer entry para volver a cargar otro dato.

    def hacerConsulta(self): # Metodo que realiza las consultas en la BD, devuelve los valores y los pone en el Treeview
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="mi_plantilla2"
        )
        micursor = mibase.cursor()
        sql = 'SELECT * FROM producto'
        micursor.execute(sql)
        resultado = micursor.fetchall() # Devuelve una lista de Tuplas con los datos.
        
        # cleaning Table 
        records = self.resumen.get_children()
        for element in records:
            self.resumen.delete(element)
        
        for x in resultado:
            self.resumen.insert('', 0, text = x[0], values = (x[1], x[2], x[3])) # primer valor, indica si el arbol tiene una rama sup
                                                            # Segunda valor es de donde empieza a guardar datos.
                                                            # Tercer valor, pongo el texto del primer valor de lista
                                                            # valor Values, pongo el resto de las columnas.
        
    def eliminarDato(self): # Metodo para eliminar datos de la DB
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="mi_plantilla2"
        )
        micursor = mibase.cursor()
        sql = "DELETE FROM producto WHERE id = %s"
        linea = self.resumen.item(self.resumen.selection())['text'] # .item devuelve un diccionario, entonces selecciono la llave 'text'
        dato = (linea,)                                             # para que me devuelva el valor.
        micursor.execute(sql, dato)
        mibase.commit()
        self.mensaje['text'] = micursor.rowcount, "Registro borrado"
       
        self.hacerConsulta()
        
    def modificarDato(self): # Metodo que crea la nueva ventana de modificacion de datos.
        # para modificar un dato en SQL debo saber los datos originales de la entrada.
        # Asique hay que pasar como parametros los datos viejos para luego modificarlos.

        self.modificarWind = Toplevel() # Nueva ventana emergente para modificar datos.
        self.modificarWind.config(bg = self.fondo)
        # Declaracion de los Entrys
        self.entradaMod1, self.entradaMod2, self.entradaMod3 = StringVar(), StringVar(), StringVar()
                
        # Funciones armado de ventana.
        def labels(texto, fila, columna):
            label = Label(self.modificarWind, text = texto, bg = self.fondo)
            label.grid(row = fila, column = columna, padx = 5)

        def entradas(variable, fila, columna):
            entry = Entry(self.modificarWind, textvariable = variable)
            entry.grid(row = fila, column = columna, padx = 5)
            return entry
        
        # Pasaje de valores para Funciones
        labels('Titulo', 0, 0)
        labels('Ruta', 1, 0)
        labels('Descripcion', 2, 0)
                
        self.entryMod1 = entradas(self.entradaMod1, 0, 1)
        self.entryMod2 = entradas(self.entradaMod2, 1, 1)
        self.entryMod3 = entradas(self.entradaMod3, 2, 1)
        self.entryMod1.focus()

        botonAgregarMod = Button(self.modificarWind, text = 'Confirmar Modificacion', command = self.confirmarMod)
        botonAgregarMod.grid(row = 3, column = 0, columnspan = 2, pady = 5)

    def confirmarMod(self): # Metodo para modificar datos de la DB
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="mi_plantilla2"
        )
        micursor = mibase.cursor()
        tituloViejo = self.resumen.item(self.resumen.selection())['values'][0] 
        rutaVieja = self.resumen.item(self.resumen.selection())['values'][1]
        descripVieja = self.resumen.item(self.resumen.selection())['values'][2]
        
        sql = ('UPDATE producto SET titulo = %s, ruta = %s, descripcion = %s' 
               'WHERE titulo = %s AND ruta = %s AND descripcion = %s')

        parametros = (self.entradaMod1.get(), self.entradaMod2.get(), self.entradaMod3.get(), tituloViejo, rutaVieja, descripVieja)
        micursor.execute(sql, parametros)
        mibase.commit()
        self.mensaje['text'] = micursor.rowcount, "Registro Modificado."
        self.hacerConsulta()
        self.modificarWind.destroy()

window = Tk()
window.config(bg = 'seashell3')
window.title('Gestion de archivos en una BD')
principal = MainWindow(window)
mainloop()