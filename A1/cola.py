class Cola:
    '''
    Una cola es una colección de elementos que no se recorren con un número
    indeterminado de los mismos. El comportamiento sigue una política FIFO
    (First In First Out). Por tanto las operaciones que soporta son.

    -- Creación de la pila
    -- Operaciones de consulta:
        - Obtener el primero de la cola
        - Comprobar si la cola está vacía
    -- Operaciones de modificación:
        - Encolar un elemento al final.
        - Desencolar el primer elemento y obtener su valor.
    '''

    def __init__(self, tipo):
        self.__cola = list()
        self.__tipo = tipo
    
    def estaVacia(self):
        return not self.__cola
    
    def primero(self):
        try:
            return self.__cola[0]
        except IndexError:
            return None
    
    def encolar(self, elemento):
        if(type(elemento) == self.__tipo):
            self.__cola.append(elemento)
            return
        else:
            raise TypeError
        
    def desencolar(self):
        try:
            return self.__cola.pop(0)
        except:
            None