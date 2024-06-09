#Clase en donde se creara todo relacionado a la gui
from tkinter import filedialog, Tk, Label, Button, Text, Canvas, ttk
from PIL import Image, ImageTk

#METODOS TEMPORALES
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de código", "*.code")])
    if archivo:
        with open(archivo, 'r') as file:
            contenido = file.read()
            print("Contenido del archivo:", contenido)
            
def ejecutar_archivo():
    print("Ejecutando Archivo")
    
#Este metodo permite guardar un reporte 
def reporte_T():
    ruta_reporte = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
    
    # Verificar si se ha seleccionado una ubicación y un nombre de archivo
    if ruta_reporte:
        try:
            # Crear el archivo con el nombre especificado en la ubicación seleccionada
            with open(ruta_reporte, 'w') as file:
                #Agregar el contenido del reporte seleccionado
                
                print("Reporte guardado en:", ruta_reporte)
        except Exception as e:
            print("Error al guardar el reporte:", e)
            
#FIN DE METODOS TEMPORALES

#Crear la ventana principal
ancho_ventana = 700
alto_ventana = 600

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

#Para cargar las imagenes
label_imagen = Label(ventana_principal, text="Imagen", bg="lightgrey", anchor="center")
label_imagen.place(x=80, y=180, width=380, height=380)

combobox = ttk.Combobox(ventana_principal)
combobox.place(x=500, y=180, width=150)

#ARCHIVOS
lbl_archivos = Label(ventana_principal, text="ARCHIVOS")
lbl_archivos.place(x=20, y=20)

#para cargar el archivo
btn_cargar_archivo = Button(ventana_principal, text="Cargar Archivo", command=cargar_archivo)
btn_cargar_archivo.place(x=20, y=60)

#para cargar el archivo
btn_ejecutar_archivo = Button(ventana_principal, text="Ejecutar Archivo", command=ejecutar_archivo)
btn_ejecutar_archivo.place(x=20, y=100)

#REPORTES 
lbl_reportes = Label(ventana_principal, text="REPORTES")
lbl_reportes.place(x= 300, y =20)

#Para mostrar reporte token
btn_reporte_token = Button(ventana_principal, text="Reporte de Tokens", command=reporte_T)
btn_reporte_token.place(x=300, y=60)

#Para reporte de errores
bnt_reporte_errores = Button(ventana_principal,text="Reporte de Errores",command=reporte_T)
bnt_reporte_errores.place(x=300,y=100)

#MOSTRAR LA VENTANA
ventana_principal.mainloop()