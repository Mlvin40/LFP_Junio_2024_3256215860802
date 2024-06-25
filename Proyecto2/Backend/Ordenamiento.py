class Ordenamiento:
    def __init__(self) -> None:
        pass
    
    # Ordenamiento de burbuja ascendente
    def burbujaAscendente(self, lista):
        for i in range(len(lista)):
            for j in range(0, len(lista)-i-1):
                if lista[j] > lista[j+1]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
        return lista
    
    # Ordenamiento de burbuja descendente
    def burbujaDescendente(self, lista):
        for i in range(len(lista)):
            for j in range(0, len(lista)-i-1):
                if lista[j] < lista[j+1]:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
        return lista
