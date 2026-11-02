"""
Módulo de Estructuras de Datos - El Archivo Perdido
Implementación de operaciones para listas, tuplas, diccionarios, conjuntos
y árbol binario de búsqueda (implementación propia, sin librerías externas).
"""

import random


# --- LISTAS (Sala de Estanterías) ---
def agregar_fragmento(inventario, fragmento):
    """Agrega un fragmento (diccionario) al inventario.

    Args:
        inventario (list): lista de fragmentos.
        fragmento (dict): fragmento a insertar.

    Returns:
        None: modifica la lista en su lugar.
    """
    inventario.append(fragmento)


def buscar_fragmento_lista(inventario, codigo):
    """Busca secuencialmente un fragmento por su código.

    Args:
        inventario (list): lista de fragmentos.
        codigo (int): código a buscar.

    Returns:
        dict | None: el fragmento encontrado o None si no existe.
    """
    for item in inventario:
        if item.get("codigo") == codigo:
            return item
    return None


def eliminar_fragmento(inventario, codigo):
    """Elimina un fragmento del inventario usando su código.

    Args:
        inventario (list): lista de fragmentos.
        codigo (int): código del fragmento a eliminar.

    Returns:
        bool: True si se eliminó, False si no existía.
    """
    item = buscar_fragmento_lista(inventario, codigo)
    if item:
        inventario.remove(item)
        return True
    return False


def ordenar_inventario_por_valor(inventario):
    """Ordena el inventario de mayor a menor según el valor del fragmento.

    Args:
        inventario (list): lista de fragmentos.

    Returns:
        None: ordena la lista en su lugar.
    """
    inventario.sort(key=lambda x: x.get("valor", 0), reverse=True)


def obtener_fragmentos_valiosos(inventario, umbral=50):
    """Filtra los fragmentos valiosos con una comprensión de listas.

    Args:
        inventario (list): lista de fragmentos.
        umbral (int): valor mínimo para considerar un fragmento valioso.

    Returns:
        list: fragmentos cuyo valor es mayor o igual al umbral.
    """
    return [f for f in inventario if f.get("valor", 0) >= umbral]


# --- TUPLAS (Sala de Mapas) ---
def crear_posicion(estante, nivel):
    """Crea una tupla inmutable (estante, nivel).

    Args:
        estante (int): número de estante.
        nivel (int): nivel dentro del estante.

    Returns:
        tuple: la posición (estante, nivel).
    """
    return (estante, nivel)


def desempaquetar_posicion(posicion):
    """Desempaqueta una tupla de posición y la describe en texto.

    Args:
        posicion (tuple): tupla (estante, nivel).

    Returns:
        str: descripción legible de la posición.
    """
    estante, nivel = posicion
    return f"Estante {estante}, Nivel {nivel}"


def asignar_posicion(fragmento):
    """Asocia a un fragmento una tupla (estante, nivel).

    Si el fragmento ya tiene posición se conserva; si no, se calcula
    de forma determinista a partir de su código.

    Args:
        fragmento (dict): fragmento al que se asigna la posición.

    Returns:
        tuple: la posición (estante, nivel) asignada.
    """
    pos = fragmento.get("posicion")
    if not isinstance(pos, tuple):
        codigo = fragmento.get("codigo", 0)
        pos = crear_posicion(codigo % 7 + 1, codigo % 4 + 1)
        fragmento["posicion"] = pos
    return pos


# --- DICCIONARIOS (Sala de Fichas) ---
def crear_fragmento_diccionario(codigo, titulo, sala, valor):
    """Crea el diccionario que representa un fragmento del catálogo.

    Args:
        codigo (int): código numérico.
        titulo (str): título del fragmento.
        sala (str): sala donde se halló.
        valor (int): valor en puntos.

    Returns:
        dict: fragmento con claves codigo, titulo, sala y valor.
    """
    return {"codigo": codigo, "titulo": titulo, "sala": sala, "valor": valor}


def consultar_campo_fragmento(fragmento, clave):
    """Consulta una clave usando get para evitar KeyError.

    Args:
        fragmento (dict): fragmento a consultar.
        clave (str): clave buscada.

    Returns:
        object | str: el valor, o un mensaje si la clave no existe.
    """
    return fragmento.get(clave, f"La clave '{clave}' no existe.")


# --- CONJUNTOS (Sala de Sellos) ---
def detectar_y_eliminar_duplicados(lista_codigos):
    """Elimina códigos repetidos convirtiendo la lista en un conjunto.

    Args:
        lista_codigos (list): códigos posiblemente repetidos.

    Returns:
        set: códigos únicos.
    """
    return set(lista_codigos)


def codigos_duplicados(lista_codigos):
    """Detecta qué códigos aparecen más de una vez, usando un conjunto.

    Args:
        lista_codigos (list): códigos a revisar.

    Returns:
        set: códigos que se repiten.
    """
    vistos = set()
    repetidos = set()
    for c in lista_codigos:
        if c in vistos:
            repetidos.add(c)
        vistos.add(c)
    return repetidos


def depurar_fragmentos(fragmentos):
    """Elimina fragmentos con código repetido usando un conjunto de códigos.

    Args:
        fragmentos (list): lista de fragmentos (diccionarios).

    Returns:
        tuple: (lista de fragmentos únicos, cantidad de descartados).
    """
    vistos = set()
    unicos = []
    for f in fragmentos:
        codigo = f.get("codigo")
        if codigo not in vistos:
            vistos.add(codigo)
            unicos.append(f)
    return unicos, len(fragmentos) - len(unicos)


def comparar_pistas_conjuntos(pistas_requeridas, pistas_jugador):
    """Compara conjuntos de pistas con intersección y diferencia.

    Args:
        pistas_requeridas (set): pistas necesarias.
        pistas_jugador (set): pistas que posee el jugador.

    Returns:
        tuple: (coincidentes, faltantes) como conjuntos.
    """
    coincidentes = pistas_requeridas.intersection(pistas_jugador)
    faltantes = pistas_requeridas.difference(pistas_jugador)
    return coincidentes, faltantes


# --- ÁRBOL BINARIO DE BÚSQUEDA (Sala Central) ---
class NodoArbol:
    """Nodo de un árbol binario de búsqueda (clave = código del fragmento)."""

    def __init__(self, fragmento):
        """Crea un nodo hoja.

        Args:
            fragmento (dict): fragmento que almacena el nodo.

        Returns:
            None
        """
        self.codigo = fragmento["codigo"]
        self.fragmento = fragmento
        self.izq = None
        self.der = None


class ArbolBinarioBusqueda:
    """Árbol binario de búsqueda implementado desde cero.

    Las operaciones son iterativas para no desbordar la pila de recursión
    cuando el árbol se degenera por inserciones ordenadas.
    """

    def __init__(self):
        """Crea un árbol vacío.

        Returns:
            None
        """
        self.raiz = None
        self.tamano = 0

    def insertar(self, fragmento):
        """Inserta un fragmento usando su código como clave.

        Args:
            fragmento (dict): fragmento con la clave 'codigo'.

        Returns:
            bool: True si se insertó, False si el código ya existía.
        """
        nuevo = NodoArbol(fragmento)
        if self.raiz is None:
            self.raiz = nuevo
            self.tamano = 1
            return True
        actual = self.raiz
        while True:
            if nuevo.codigo == actual.codigo:
                return False
            if nuevo.codigo < actual.codigo:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
        self.tamano += 1
        return True

    def buscar(self, codigo):
        """Busca un fragmento por código contando las comparaciones.

        Args:
            codigo (int): código a buscar.

        Returns:
            tuple: (fragmento o None, número de comparaciones).
        """
        actual = self.raiz
        comparaciones = 0
        while actual is not None:
            comparaciones += 1
            if codigo == actual.codigo:
                return actual.fragmento, comparaciones
            actual = actual.izq if codigo < actual.codigo else actual.der
        return None, comparaciones

    def inorden(self):
        """Recorre el árbol en inorden (izquierda, raíz, derecha).

        Returns:
            list: fragmentos en el orden del recorrido.
        """
        resultado = []
        pila = []
        actual = self.raiz
        while pila or actual is not None:
            while actual is not None:
                pila.append(actual)
                actual = actual.izq
            actual = pila.pop()
            resultado.append(actual.fragmento)
            actual = actual.der
        return resultado

    def altura(self):
        """Calcula la altura del árbol (nodos del camino más largo).

        Returns:
            int: altura; 0 si el árbol está vacío.
        """
        if self.raiz is None:
            return 0
        nivel = [self.raiz]
        altura = 0
        while nivel:
            altura += 1
            siguiente = []
            for nodo in nivel:
                if nodo.izq:
                    siguiente.append(nodo.izq)
                if nodo.der:
                    siguiente.append(nodo.der)
            nivel = siguiente
        return altura


def buscar_secuencial(lista, codigo):
    """Búsqueda secuencial por código contando comparaciones.

    Args:
        lista (list): lista de fragmentos.
        codigo (int): código a buscar.

    Returns:
        tuple: (fragmento o None, número de comparaciones).
    """
    comparaciones = 0
    for item in lista:
        comparaciones += 1
        if item.get("codigo") == codigo:
            return item, comparaciones
    return None, comparaciones


def esta_ordenada(fragmentos):
    """Verifica que una lista de fragmentos esté ordenada por código.

    Args:
        fragmentos (list): fragmentos a verificar.

    Returns:
        bool: True si los códigos son estrictamente crecientes.
    """
    codigos = [f["codigo"] for f in fragmentos]
    return all(codigos[i] < codigos[i + 1] for i in range(len(codigos) - 1))


def comparar_busquedas(tamano, ordenado=False):
    """Compara el promedio de comparaciones entre árbol y búsqueda secuencial.

    Busca cada código del catálogo sintético una vez.

    Args:
        tamano (int): cantidad de fragmentos del catálogo de prueba.
        ordenado (bool): si es True se inserta en orden creciente
            (el árbol se degenera en una lista enlazada).

    Returns:
        dict: tamano, altura, promedio_arbol y promedio_secuencial.
    """
    codigos = list(range(1, tamano + 1))
    if not ordenado:
        random.shuffle(codigos)
    lista = [{"codigo": c} for c in codigos]
    arbol = ArbolBinarioBusqueda()
    for f in lista:
        arbol.insertar(f)
    total_arbol = 0
    total_sec = 0
    for c in range(1, tamano + 1):
        total_arbol += arbol.buscar(c)[1]
        total_sec += buscar_secuencial(lista, c)[1]
    return {
        "tamano": tamano,
        "altura": arbol.altura(),
        "promedio_arbol": total_arbol / tamano,
        "promedio_secuencial": total_sec / tamano,
    }
