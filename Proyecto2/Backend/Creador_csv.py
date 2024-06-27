import pandas as pd

class ExportadorCSV:
    
    def __init__(self):
        pass
    
    # Metodo que exporta los datos a un archivo CSV
    def exportar(self, datos, direccion):
        # Convertir la lista a DataFrame
        lista = []
        for numero in datos:
            lista.append(numero.lexema)  
            
        # Quitar las comillas de la ruta para evitar errores
        ruta = direccion.strip('"')
        
        df = pd.DataFrame(lista, columns=['Date'])
        
        # Exportar a CSV
        df.to_csv(ruta, index=False)
 