import sys
import os
# Añade la ruta del directorio principal al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from Frontend.VentanaAplicacion import VentanaAplicacion
except:
    print("Fin Aplicacion")