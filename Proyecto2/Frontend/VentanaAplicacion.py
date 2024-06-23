from tkinter import filedialog, Tk, Label, Button, Canvas, ttk, messagebox, Text, Scrollbar
from PIL import Image, ImageTk


def cargar_archivo():
    print("Cargando archivo")
    
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
    print("Ejecutando archivo")
    
def reporte_T(tipo):
    print("Generando reporte")
  
def mostrar(event):
    print("Mostrando ")
    

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
anchoTexto = 620
altoTexto = 420
textbox = Text(ventana_principal, bg="lightgrey")
textbox.place(x=100, y=200, width=anchoTexto, height=altoTexto)

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

