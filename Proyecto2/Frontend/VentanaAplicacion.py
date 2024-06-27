import sys
import os
# Añade la ruta del directorio principal al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tkinter import filedialog, Tk, Label, Button, Canvas, ttk, messagebox, Text, Scrollbar
from PIL import Image, ImageTk
from Backend.Sintaxis import Parser as ParserClass
from Backend.Lexer import Lexer as LexerClass

contenido_archivo = ""
    
def cargar_archivo():
    global contenido_archivo
    print("Cargando archivo")
    
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de código", "*.lfp")])
    if archivo:
        with open(archivo, 'r', encoding= 'utf-8') as file:
            btn_ejecutar_archivo.configure(state="normal") # Habilitar el botón de ejecutar
            contenido_archivo = file.read() #Si ya habia contenido en el archivo se sobreescribe
            textbox.insert("1.0", contenido_archivo)
            messagebox.showinfo("Mensaje", "Archivo cargado correctamente.")
    
def reiniciar_atributos():
    print("Reiniciando atributos")

def obtener_contenido():
    global contenido_archivo
    # Obtener el contenido del textbox
    contenido_archivo = textbox.get("1.0", "end-1c")
    
def ejecutar_archivo():
    lexer = LexerClass() # Instanciar un objeto de la clase Lexer
    obtener_contenido()
    print(contenido_archivo)
    
    lexer.analizar(contenido_archivo)
     
    parser = ParserClass(lexer.tokens, lexer.token_errors) # Instanciar un objeto de la clase Parser
    parser.parse()
    parser.realizar_acciones()
    if parser.hay_errores():
        messagebox.showerror("Error", "Se encontraron errores en el archivo.")
    else:
        messagebox.showinfo("Mensaje", "Archivo ejecutado correctamente.")
    
def reporte_T(tipo):
    print("Generando reporte")

def mostrar(event):
    print("Mostrando")
    
# Crear la ventana principal
ancho_ventana = 860
alto_ventana = 740

ventana_principal = Tk()
ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}")
ventana_principal.title("LFP - Proyecto Final")

# Cargar la imagen para el fondo
imagen = Image.open('fondoApp.jpg')
imagen = imagen.resize((ancho_ventana, alto_ventana), Image.LANCZOS)
fondo = ImageTk.PhotoImage(imagen)

canva = Canvas(ventana_principal, width=ancho_ventana, height=alto_ventana)
canva.pack(fill="both", expand=True)
canva.create_image(0, 0, image=fondo, anchor="nw")

# Para crear el textbox para mostrar el contenido del archivo
anchoTexto = 680
altoTexto = 420
textbox = Text(ventana_principal, bg="lightgrey")
textbox.place(x=80, y=200, width=anchoTexto, height=altoTexto)

# ARCHIVOS
lbl_archivos = Label(ventana_principal, text="ARCHIVOS")
lbl_archivos.place(x=20, y=20)

# Para abrir el archivo
btn_abrir_archivo = Button(ventana_principal, text="Abrir Archivo", command=cargar_archivo)
btn_abrir_archivo.place(x=20, y=60)

# Para ejecutar el archivo
btn_ejecutar_archivo = Button(ventana_principal, text="Ejecutar Archivo", command=ejecutar_archivo)
btn_ejecutar_archivo.place(x=360, y=640)

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
