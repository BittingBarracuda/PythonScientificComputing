from pila import Pila
from cola import Cola

class ArbolBinario:
    def __init__(self):
        self._raiz = None
        self._arbolIzdo = None
        self._arbolDcho = None
    
    def raiz(self):
        return self._raiz
    def arbolIzdo(self):
        return self._arbolIzdo
    def arbolDcho(self):
        return self._arbolDcho
    
    def estaVacio(self):
        return self._raiz == None

    # Métodos protegidos para construir subárboles pasados por parámetro
    def _insertarArbolIzq(self, arbIzq):
        self._arbolIzdo = arbIzq
    
    def _insertarArbolDcho(self, arbDcho):
        self._arbolDcho = arbDcho
    
    # Este metodo inserta un elemento en el arbol binario buscando
    # por amplitud el primer hueco disponible
    def insertarElemento(self, elemento):
        # Si el arbol actual está vació, guardamos el elemento en su raiz
        # y generamos sus subárboles izquierdo y derecho
        if self.estaVacio():
            self._raiz = elemento
            self._arbolIzdo = ArbolBinario()
            self._arbolDcho = ArbolBinario()
        # En caso contrario hacemos un recorrido en amplitud e insertamos
        # en el primer hueco que nos encontremos
        else:
            c = Cola(type(self))
            c.encolar(self)
            while not c.estaVacia():
                actual = c.desencolar()
                if  actual._arbolIzdo.estaVacio():
                    actual._arbolIzdo.insertarElemento(elemento)
                    return
                else:
                    c.encolar(actual._arbolIzdo)

                if actual._arbolDcho.estaVacio():
                    actual._arbolDcho.insertarElemento(elemento)
                    return
                else:
                    c.encolar(actual._arbolDcho)
    
    def tieneElemento(self, elemento):
        if not self.estaVacio():
            if self._raiz == elemento:
                return True
            else:
                return self._arbolIzdo.tieneElemento(elemento) or self._arbolDcho.tieneElemento(elemento)
        else:
            return False

    def numElementos(self):
        if self.estaVacio():
            return 0
        else:
            return 1 + self._arbolIzdo.numElementos() + self._arbolDcho.numElementos()

    def preOrden(self):
        l = []
        l.append(self._raiz)
        if not self._arbolIzdo.estaVacio():
            l += self._arbolIzdo.preOrden()
        if not self._arbolDcho.estaVacio():
            l += self._arbolDcho.preOrden()
        return l
    
    def inOrden(self):
        l =  []
        if not self._arbolIzdo.estaVacio():
            l += self._arbolIzdo.inOrden()
        l.append(self._raiz)
        if not self._arbolDcho.estaVacio():
            l += self._arbolDcho.inOrden()
        return l
    
    def preOrdenIterativo(self):
        '''
        La idea de este método consiste en comenzar recorriendo el árbol hacia la izquierda e ir guardando los
        nodos que se visiten (los guardaremos en l para denotar que están visitados). Para seguir el 
        orden raiz -> sub-arbol izq -> sub-arbol dcho usamos una pila en la que acumulamos primero los hijos derechos 
        y luego los izquierdos del nodo que estemos visitando (esto es así porque luego al desapilar por la política 
        FIFO obtendremos primero los izquierdos). 
        '''
        # Generamos la pila como estructura auxiliar para el recorrido y la lista a devolver vacía
        p = Pila(type(self))
        l = []
        if not self.estaVacio():
            # Apilamos el elemento raíz
            p.apilar(self)
            # Mientras que queden elementos en la pila iteraremos
            while not p.estaVacia():
                # Desapilaremos el primer elemento y lo marcaremos como visitado guardándolo en l
                actual = p.desapilar()
                l.append(actual._raiz)
                # Si el nodo actual tiene hijos por la derecha apilaremos el sub-árbol derecho
                if not actual._arbolDcho.estaVacio():
                    p.apilar(actual._arbolDcho)
                # Si el nodo actual tiene hijos por la izquierda apilaremos el sub-árbol izquierdo
                if not actual._arbolIzdo.estaVacio():
                    p.apilar(actual._arbolIzdo)
                # De esta forma garantizamos que en la siguiente iteración desapilaremos siempre primero 
                # los hijos izquierdos. En caso de que no existan, desapilaremos los derechos. Y en caso de que
                # tampoco existan volveremos a los nodos de niveles superiores (más cercanos a la raíz)
        return l
    
    def inOrdenIterativo(self):
        '''
        La idea de este método consiste en comenzar recorriendo el árbol siempre hacia la izquierda.
        Para seguir el orden sub-arbol izq -> raiz -> sub-arbol dcho usamos una pila en la que vamos
        acumulando los nodos por los que vamos pasando. Cuándo lleguemos a un nodo en el que NO podamos
        seguir a la izquierda entonces, lo desapilaremos de p, lo guardaremos en la lista l (denotando
        que lo hemos visitado) y seguiremos por su hijo derecho (en caso de que sea posible, si no es 
        posible tendremos que volver a su nodo padre). A partir de aquí la idea es repetir este proceso
        es decir, aunque estemos visitando un hijo derecho intentaremos siempre continuar por la izquierda.
        '''
        # Generamos la pila como estructura auxiliar para el recorrido y la lista a devolver vacía
        p = Pila(type(self))
        l = []
        # Apilamos el nodo raíz e incializamos la variable actual también al nodo raíz
        # La variable actual nos indica en que nodo nos encontramos en cada momento.
        if not self.estaVacio():
            p.apilar(self)
            actual = self
            # La variable booleana fin_rama sirve para indicar que hemos visitado completamente
            # algún sub-árbol (es decir, hemos llegado a un punto dónde no hay ni hijos izq. ni dchos.)
            # En ese caso, utilizamos esa variable para indicarle al padre del nodo visitado que 
            # no se debe continuar descendiendo por esa rama
            fin_rama = False
            # Siempre que queden elementos en la pila seguimos iterando
            while not p.estaVacia():
                # Si el nodo actual tiene hijos por la izquierda y esos nodos no hayan
                # sido completamente visitados (fin_rama), los apilamos en p
                # y cambiamos el nodo actual a ese hijo izquierdo.
                if not actual._arbolIzdo.estaVacio() and not fin_rama:
                    p.apilar(actual._arbolIzdo)
                    actual = actual._arbolIzdo
                # En caso de que el nodo actual no tenga hijos por la izquierda (o ya hayan sido visitados)
                # lo desapilamos de p y lo introducimos en l (de esta forma indicamos
                # que lo hemos visitado pues si no tiene hijos izquierdos hay que 
                # visitar la raíz).
                else:
                    actual = p.desapilar()
                    l.append(actual._raiz)
                    # Ahora pueden ocurrir dos cosas
                    # O bien el nodo actual tiene hijos derechos por lo que continuamos
                    # por la derecha
                    if not actual._arbolDcho.estaVacio():
                        p.apilar(actual._arbolDcho)
                        actual = actual._arbolDcho
                        # En caso de que se tengan hijos por la derecha entonces no hemos
                        # recorrido completamente ese subárbol y ponemos fin_rama a False
                        fin_rama = False
                    # O bien el nodo actual tampoco tiene hijos derechos por lo que
                    # debemos volver a su nodo padre que estará en la cima de la 
                    # pila p.
                    else:
                        actual = p.cima()
                        # Si el nodo no tiene ni hijos izquierdos ni derechos hemos visitado
                        # completamente ese sub-árbol y ponemos fin-rama a true
                        fin_rama = True
            return l

    def amplitudIterativo(self):
        # Generamos una cola como estructura auxiliar y la lista a devolver vacía
        c = Cola(type(self))
        l = []
        # Si el árbol no está vacío
        if not self.estaVacio():
            # Encolamos la raíz
            c.encolar(self)
            # Mientras la cola no esté vacía iteraremos
            while not c.estaVacia():
                # Obtendremos el nodo actual que será el primero de la cola
                actual = c.desencolar()
                # Lo guardamos en l para indicar que lo hemos visitado
                l.append(actual._raiz)
                # Si el nodo actual tiene sub-arbol izquierdo lo encolamos
                if not actual._arbolIzdo.estaVacio():
                    c.encolar(actual._arbolIzdo)
                # Si el nodo actual tiene sub-árbol derecho lo encolamos
                if not actual._arbolDcho.estaVacio():
                    c.encolar(actual._arbolDcho)
                # De esta forma garantizamos que para cierto nodo, siempre 
                # visitaremos en primer lugar su hijo izquierdo (si existe)
                # y luego su hijo derecho (también si existe) antes de pasar
                # a niveles inferiores del árbol.
        return l


class ArbolBinarioOrdenado(ArbolBinario):
    def __init__(self):
        super().__init__()

    def insertarElem(self, elemento):
        if self.estaVacio():
            self._raiz = elemento
            self._arbolIzdo = ArbolBinarioOrdenado()
            self._arbolDcho = ArbolBinarioOrdenado()
        elif elemento <= self._raiz:
            self._arbolIzdo.insertarElem(elemento)
        elif elemento > self._raiz:
            self._arbolDcho.insertarElem(elemento)
        else:
            None
    
    def tieneElemento(self, elemento):
        if self.estaVacio():
            return False
        elif self._raiz == elemento:
            return True
        elif elemento < self._raiz:
            self._arbolIzdo.tieneElemento(elemento)
        else:
            self._arbolDcho.tieneElemento(elemento)

class ArbolHuffman(ArbolBinario):
    def __init__(self, dic = None):
        super().__init__()
        # Con el objetivo de poder realizar un recorrido del arbol "hacia arriba"
        # un arbol de Huffman tendrá un nuevo atributo self._padre. Este atributo
        # hará referencia al nodo padre lo que nos permitirá acceder fácilmenta al mismo
        self._padre = None
        # Añadimos un atributo para representar el codigo del nodo (0 o 1)
        self._codigo = ""
        # Añadimos un atributo para representar el símbolo del nodo
        self._simbolo = ""
        # Añadimos un atributo para representar la frecuencia del nodo
        self._frec = None
        if dic != None:
            self.__construirArbol(dic)
    

    # Método privado auxiliar
    def __tienePadre(self):
        return self._padre != None

    def insertarElemento(self, simbolo, frec):
        self._raiz = (simbolo, frec)
        self._simbolo = simbolo
        self._frec = frec
        self._arbolIzdo = ArbolHuffman()
        self._arbolDcho = ArbolHuffman()
    
    def __construirArbol(self, dic):
        arboles = []
        # Creamos el conjunto de hojas asociados a cada símbolo del diccionario
        for (sym, frec) in dic.items():
            # Cada hoja no es más que un árbol binario con un nodo
            # con insertarElemento(...) almacenamos en el nodo
            # el simbolo que representa y la frecuencia
            ab = ArbolHuffman()
            ab.insertarElemento(sym, frec)
            arboles.append(ab)
        # Para asegurarnos que tomamos siempre los valores de mínima
        # frecuencia ordenamos ascendentemente de acuerdo a los valores
        # de frecuencia.
        arboles.sort(key = lambda arbol: arbol._frec)
        
        # Por conveniencia en el método de codificación, vamos a guardar un atributo
        # self._hojas dónde almacenaremos las hojas del árbol. De esta forma tendremos
        # accesibles de forma rápida los símbolos que se han codificado. Para ello
        # realizamos una copia de arboles (así evitamos que al modificar la lista arboles
        # se modifique este atributo).
        self._hojas = arboles.copy()

        # Procedemos a generar el arbol de Huffman
        while len(arboles) > 1:
            # Tomamos el árbol o nodo con menor valor de frecencia
            ab1 = arboles.pop(0)
            # Este arbol será el subárbol izquierdo del nuevo árbol a generar
            # por tanto, irá asociado con el código 0
            ab1._codigo = '0'
            # Tomamos el siguiente árbol o nodo con menor valor de frecuencia
            ab2 = arboles.pop(0)
            # Este arbol será el subárbol derecho del nuevo árbol a generar
            # por tanto, irá asociado con el código 1
            ab2._codigo = '1'
            ab1._raiz = ab1._raiz + (ab1._codigo,)
            ab2._raiz = ab2._raiz + (ab2._codigo,)
            # Creamos el árbol padre
            ab_padre = ArbolHuffman()
            # En este árbol el simbolo no resulta importante y la frecuencia resulta
            # de la suma de las frecuencias de sus hijos
            ab_padre.insertarElemento("", ab1._frec + ab2._frec)
            # Insertamos sus hijos ab1 -> izquierda, ab2 -> derecha
            ab_padre._insertarArbolIzq(ab1); ab_padre._insertarArbolDcho(ab2)
            # Añadimos a los hijos la referencia a su arbol padre
            ab1._padre = ab_padre; ab2._padre = ab_padre
            # Guardamos el árbol padre en la lista de árboles y reordenamos
            # de nuevo de acuerdo a los valores de frencuencia.
            arboles.append(ab_padre)
            arboles.sort(key = lambda arbol: arbol._frec)
        
        self._raiz = (arboles[0]._simbolo, arboles[0]._frec)
        self._frec = arboles[0]._frec
        self._arbolIzdo = arboles[0]._arbolIzdo
        self._arbolDcho = arboles[0]._arbolDcho

    def decodificar(self, codigo):
        aux = self
        # Recorremos la entrada dígito a dígito
        for digito in codigo:
            # Si el dígito es un 0 continuamos por el subarbol izquierdo
            if digito == '0':
                aux = aux._arbolIzdo
            # Si el digito en un 1 continuamos por el subarbol derecho
            elif digito == '1':
                aux = aux._arbolDcho
            # En otro caso consideramos que el código está mal formado y
            # lanzamos una excepción
            else:
                raise ValueError
            # Si el subárbol en el que nos encontramos está vacío significa
            # que el código no nos lleva a ningún símbolo y devolvemos None
            if aux.estaVacio():
                return None
        # Nos aseguramos que efectivamente hemos llegado a un nodo hoja que 
        # representa un símbolo codificado
        if (aux._simbolo != ""):
            return aux._simbolo
        # En caso contrario devolvemos None
        else:
            return None
    
    def codificar(self, simbolo):
        # Empezamos buscando en la lista self._hojas si existe algún nodo que represente
        # al simbolo pasado como argumento
        nodo_hoja = [nodo for nodo in self._hojas if nodo._simbolo == simbolo]
        # En caso de que no se encuentre devolvemos None
        if not nodo_hoja:
            return None
        else:
            nodo = nodo_hoja[0]
            # Tomamos el código correspondiente a este nodo
            codigo = nodo._codigo
            # Comenzamos a recorrer el arbol hacia arriba hasta encontrar
            # la raíz. Sabemos que un nodo es el raíz porque su padre es None
            while nodo.__tienePadre():
                nodo = nodo._padre
                # Añadimos "por la izquierda" el codigo del nuevo nodo
                # que estamos visitando.
                codigo = nodo._codigo + codigo
            return codigo


if __name__ == "__main__":
    # Pruebas para los recorridos el árbol binario ordenado
    abo = ArbolBinarioOrdenado()
    elems = [8, 3, 1, 6, 4, 7, 10, 14, 13]
    for elem in elems:
        abo.insertarElem(elem)
    print(f"Pre Orden Recursivo -> {abo.preOrden()}")
    print(f"Pre Orden Iterativo -> {abo.preOrdenIterativo()}")
    print(f"In Orden Recursivo -> {abo.inOrden()}")
    print(f"In Orden Iterativo -> {abo.inOrdenIterativo()}")
    print(f"Recorrido en amplidud -> {abo.amplitudIterativo()}")

    # Pruebas para el árbol de Huffman
    dic = {"A":0.15, "B":0.3, "C":0.2, "D":0.05, "E":0.15, "F":0.05, "G":0.10}
    ah = ArbolHuffman(dic)
    print(ah.amplitudIterativo())
    codigos = []
    for sym in dic.keys():
        codigo = ah.codificar(sym)
        codigos.append(codigo)
        print(f"Codigo para {sym} -> {codigo}")
    print("\n\n")
    for codigo in codigos:
        print(f"Simbolo de {codigo} -> {ah.decodificar(codigo)}")
    