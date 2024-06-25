import pandas as pd

class ExportadorCSV:
    
    def __init__(self):
        pass
    
    
    def exportar(self, datos, direccion):
        # Convertir la lista a DataFrame
        
        lista = []
        for numero in datos:
            lista.append(numero.lexema)  
            
        ruta = direccion.strip('"')
        
        df = pd.DataFrame(lista, columns=['Datos'])
        
        # Exportar a CSV
        df.to_csv(ruta, index=False)
 
"""        
# Lista de números
numeros = [1, 2, 3, -4, 5.12]

# Convertir la lista a DataFrame
df = pd.DataFrame(numeros, columns=['Numeros'])

# Exportar a CSV
df.to_csv('lista_numeros.csv', index=False)
"""