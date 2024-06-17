from tkinter import filedialog, Tk, Label, Button, Canvas, ttk, messagebox
from PIL import Image, ImageTk
from Backend.Lexer import Lexer
from Backend.Grafo import Grafo
from Backend.Reportes import Reporte

# Variables globales
contenido_archivo = ""
cantidad_grafos = 0
grafo = Grafo()

def cargar_archivo():
    global contenido_archivo, btn_ejecutar_archivo
    
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de código", "*.code")])
    if archivo:
        with open(archivo, 'r', encoding= 'utf-8') as file:
            btn_ejecutar_archivo.configure(state="normal") # Habilitar el botón de ejecutar
            contenido_archivo = file.read() #Si ya habia contenido en el archivo se sobreescribe
            messagebox.showinfo("Mensaje", "Archivo cargado correctamente.")
            
def reiniciar_atributos():
    global label_imagen, combobox
    label_imagen.config(image="")
    label_imagen.config(text="Imagen")
    combobox.set("")
    combobox['values'] = []
    
def ejecutar_archivo():
    reiniciar_atributos() # Reiniciar los atributos del archivo anterior si es que existen
    global contenido_archivo, cantidad_grafos
    grafo.lexer.reiniciar_listas() #Reinicia los errores del archivo anterior
    grafo.lexer.analizar(contenido_archivo)
    
    # Si no encuentra errores se crean los grafos
    if len(grafo.lexer.errores) > 0:
        messagebox.showerror("Errores léxicos encontrados","Corrija los errores léxicos en el archivo de entrada para poder crear los grafos. \nCantidad de errores encontrados: "+str(len(grafo.lexer.errores)))
        return
    
    grafo.escanear_tokens(contenido_archivo)
    cantidad_grafos = len(grafo.imagenes_procesadas)
    messagebox.showinfo("Mensaje", f"Grafos creados correctamente.\nCantidad de grafos encontrados: {cantidad_grafos}")
    print("Cantidad de grafos encontrados:", cantidad_grafos)
    
    # Actualizar el combobox con los nombres de los grafos
    actualizar_combobox()

def actualizar_combobox():
    global grafo
    #arreglo que almacena los nombres de los grafos
    nombres_grafos = []
    for imagen in grafo.imagenes_procesadas:
        nombre = imagen["nombre"].strip("'")#Se elimina la comilla simple del nombre
        nombres_grafos.append(nombre)
    
    #se actualiza el combobox con los nombres de los grafos
    combobox['values'] = nombres_grafos
    
def mostrar_grafo(event):
    global grafo, label_imagen
    seleccion = combobox.current()
    print("Mostrando grafo:", seleccion)
    grafo.mostrar_grafo(seleccion, label_imagen)
    
def reporte_T(tipo):
    #Tipo 1 = Reporte de Tokens Tipo 2 = Reporte de Errores
    ruta_reporte = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
    if ruta_reporte:
        try:
            with open(ruta_reporte, 'w') as file:
                if tipo == 1:
                    Lista = []
                    for imagen in grafo.lexer.lista_imagenes:
                        for token in imagen:
                            Lista.append(token)                 
                    gen = Reporte(Lista, "Tokens")
                else:
                    gen = Reporte(grafo.lexer.errores, "Errores")
                    
                html = gen.obtenerReporte()
                file.write(html)
                print("Reporte guardado en:", ruta_reporte)
                messagebox.showinfo("Mensaje", f"Reporte creado exitosamente. \nReporte guardado en: {ruta_reporte}")
                
        except Exception as e:
            print("Error al guardar el reporte:", e)
            
# Crear la ventana principal
ancho_ventana = 860
alto_ventana = 760

ventana_principal = Tk()
ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}")
ventana_principal.title("Grafos de Guatemala")

# Cargar la imagen para el fondo
imagen = Image.open('fondoventana.jpg')
imagen = imagen.resize((ancho_ventana, alto_ventana), Image.LANCZOS)
fondo = ImageTk.PhotoImage(imagen)

canva = Canvas(ventana_principal, width=ancho_ventana, height=alto_ventana)
canva.pack(fill="both", expand=True)
canva.create_image(0, 0, image=fondo, anchor="nw")

# Para cargar las imágenes
label_imagen = Label(ventana_principal, text="Imagen", bg="lightgrey", anchor="center")
label_imagen.place(x=40, y=160, width=520, height=520)

combobox = ttk.Combobox(ventana_principal)
combobox.place(x=600, y=160, width=150)
combobox.bind("<<ComboboxSelected>>", mostrar_grafo)

# ARCHIVOS
lbl_archivos = Label(ventana_principal, text="ARCHIVOS")
lbl_archivos.place(x=20, y=20)

# Para cargar el archivo
btn_cargar_archivo = Button(ventana_principal, text="Cargar Archivo", command=cargar_archivo)
btn_cargar_archivo.place(x=20, y=60)

# Para ejecutar el archivo
btn_ejecutar_archivo = Button(ventana_principal, text="Ejecutar Archivo", command=ejecutar_archivo, state="disabled")
btn_ejecutar_archivo.place(x=20, y=100)

# REPORTES 
lbl_reportes = Label(ventana_principal, text="REPORTES")
lbl_reportes.place(x=300, y=20)

# Para mostrar reporte de tokens
btn_reporte_token = Button(ventana_principal, text="Reporte de Tokens", command= lambda:reporte_T(1))
btn_reporte_token.place(x=300, y=60)

# Para reporte de errores
bnt_reporte_errores = Button(ventana_principal, text="Reporte de Errores", command= lambda:reporte_T(2))
bnt_reporte_errores.place(x=300, y=100)

# Mostrar la ventana
ventana_principal.mainloop()