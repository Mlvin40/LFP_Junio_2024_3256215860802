#clase donde se crea la interfaz grafica de la aplicacion
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Backend.Reportes import Reporte
from Backend.Lexer import Lexer

from Frontend.VentanaAplicacion import VentanaAplicacion
VentanaAplicacion().mainloop()
