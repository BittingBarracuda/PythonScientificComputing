class Pila:
    '''
    TAD Pila

    Una pila es una estructura de elementos que no se puede recorrer con un
    número indeterminado de los mismos. Su comportamiento sigue una política
    LIFO (Last In First Out) por tanto las operaciones que debe soportar son.

    -- Creación de la pila
    -- Operaciones de consulta:
        - Obtener la cima de la pila.
        - Comprobar si está vacía
    -- operaciones de modificación:
        -- Apilar un elemento en la cima
        -- Desapilar un elemento de la cima y obtener su valor
    '''

    def __init__(self, tipo):
        self.__pila = list()
        self.__tipo = tipo
    
    def estaVacia(self):
        return not self.__pila
    
    def cima(self):
        try:
            return self.__pila[-1]
        except IndexError:
            return None
    
    def apilar(self, elemento):
        if(type(elemento) == self.__tipo):
            self.__pila.append(elemento)
            return
        else:
            raise TypeError
    
    def desapilar(self):
        try:
            return self.__pila.pop()
        except:
            None
    
    def __str__(self):
        return str(self.__pila)