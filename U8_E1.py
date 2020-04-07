from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

import mysql.connector # Importo el conector de MySQL (antes se lo descargó con pip install mysql-connector)
              
class MainWindow: # Clase principal contenedora de todos las funciones del programa.
    def __init__(self, root): # Constructor de la clase.
        # Creacion y Grindeado de los Frames
        self.Frame1 = Frame(root)
        self.Frame1.grid(row = 0, column = 0)
        self.Frame2 = LabelFrame(root, text = 'Lista de cargados')
        self.Frame2.grid(row = 1, column = 0, columnspan = 2)
        self.Frame3 = Frame(root)
        self.Frame3.grid(row = 0, column = 1)
                
        # Declaracion de los Entrys
        self.entrada1, self.entrada2, self.entrada3 = StringVar(), StringVar(), StringVar()
                
        # Funciones armado de ventana.
        def labels(texto, fila, columna):
            label = Label(self.Frame1, text = texto)
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
            
        # Botones
        botonAgregar = Button(self.Frame1, text = 'Guardar Datos', command = self.agregaraDB) # Boton para grabar datos en BD
        botonAgregar.grid(row = 3, column = 1, pady = 5)

        botonCrearBD = Button(self.Frame3, text = 'Crear BD', command = self.crearBase) # Boton para crear Base si no existe
        botonCrearBD.grid(row = 0, column = 0, padx = 5)

        botonCrearTabla = Button(self.Frame3, text = 'Crear Tabla', command = self.crearTB) # Boton para crear Tabla si no existe.
        botonCrearTabla.grid(row = 0, column = 1)

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
                print('La Base de Datos ya está creada.')
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
                print('La lista ya está creada.')
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
             print ("No cargaste ningun dato")                                              # y muetra un mensaje de error.
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
                self.entry1.focus() # Cuando se agregan los datos vuelve al primer entry para volver a cargar otro dato.

    def hacerConsulta(self):
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="mi_plantilla2"
        )
        micursor = mibase.cursor()
        sql = 'SELECT * FROM producto'
        micursor.execute(sql)
        resultado = micursor.fetchall()
        
        # cleaning Table 
        records = self.resumen.get_children()
        for element in records:
            self.resumen.delete(element)
        
        for x in resultado:
            self.resumen.insert('', 0, text = x[0], values = (x[1], x[2], x[3])) # primer valor, indica si el arbol tiene una rama sup
                                                            # Segunda valor es de donde empieza a guardar datos.
                                                            # Tercer valor, pongo el texto del primer valor de lista
                                                            # valor Values, pongo el resto de las columnas.
        
window = Tk()
window.title('Ejercicio unidad 8 - Jaimovich Andrés')
principal = MainWindow(window)
mainloop()