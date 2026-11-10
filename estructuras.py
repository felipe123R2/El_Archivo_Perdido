"""
Módulo de Estructuras de Datos - El Archivo Perdido
Listas, tuplas, diccionarios, conjuntos y árbol binario de búsqueda
(implementación propia, sin librerías externas).
"""

import random
from collections import deque


# --- LISTAS (Sala de Estanterías) ---
def agregar_fragmento(inventario, fragmento):
    """Agrega un fragmento al final del inventario (append).

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
    """Elimina un fragmento del inventario usando su código (remove).

    Args:
        inventario (list): lista de fragmentos.
        codigo (int): código del fragmento a eliminar.

    Returns:
        bool: True si se eliminó, False si no existía.
    """
    item = buscar_fragmento_lista(inventario, codigo)
    if item:
        inventario.remove(item)
    return item is not None


def ordenar_inventario_por_valor(inventario):
    """Ordena el inventario de mayor a menor valor (sort con reverse).

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
    """Desempaqueta la tupla de posición y la describe en texto.

    Args:
        posicion (tuple): tupla (estante, nivel).

    Returns:
        str: descripción legible de la posición.
    """
    estante, nivel = posicion
    return f"Estante {estante}, Nivel {nivel}"


def asignar_posicion(fragmento):
    """Asocia al fragmento una tupla (estante, nivel); si ya la tiene, la conserva.

    Args:
        fragmento (dict): fragmento al que se asigna la posición.

    Returns:
        tuple: la posición (estante, nivel) del fragmento.
    """
    if not isinstance(fragmento.get("posicion"), tuple):
        codigo = fragmento.get("codigo", 0)
        fragmento["posicion"] = crear_posicion(codigo % 7 + 1, codigo % 4 + 1)
    return fragmento["posicion"]


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
    """Consulta una clave con get para evitar KeyError.

    Args:
        fragmento (dict): fragmento a consultar.
        clave (str): clave buscada.

    Returns:
        object | str: el valor, o un mensaje si la clave no existe.
    """
    return fragmento.get(clave, f"La clave '{clave}' no existe.")


def indexar_por_codigo(inventario):
    """Crea un diccionario {código: fragmento} con una comprensión de diccionario.

    Args:
        inventario (list): lista de fragmentos.

    Returns:
        dict: fragmentos indexados por su código.
    """
    return {f["codigo"]: f for f in inventario}


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
    """Detecta los códigos que aparecen más de una vez (count).

    Args:
        lista_codigos (list): códigos a revisar.

    Returns:
        set: códigos que se repiten.
    """
    return {c for c in lista_codigos if lista_codigos.count(c) > 1}


def depurar_fragmentos(fragmentos):
    """Elimina fragmentos con código repetido usando un conjunto de códigos.

    Args:
        fragmentos (list): lista de fragmentos (diccionarios).

    Returns:
        tuple: (lista de fragmentos únicos, cantidad de descartados).
    """
    vistos, unicos = set(), []
    for f in fragmentos:
        if f.get("codigo") not in vistos:
            vistos.add(f.get("codigo"))
            unicos.append(f)
    return unicos, len(fragmentos) - len(unicos)


def comparar_pistas_conjuntos(pistas_requeridas, pistas_jugador):
    """Compara las pistas con intersección (&) y diferencia (-).

    Args:
        pistas_requeridas (set): pistas necesarias.
        pistas_jugador (set): pistas que posee el jugador.

    Returns:
        tuple: (coincidentes, faltantes) como conjuntos.
    """
    return pistas_requeridas & pistas_jugador, pistas_requeridas - pistas_jugador


# --- ÁRBOL BINARIO DE BÚSQUEDA (Sala Central) ---
class NodoArbol:
    """Nodo de un árbol binario de búsqueda (clave = código, valor = fragmento)."""

    def __init__(self, fragmento):
        """Crea un nodo hoja.

        Args:
            fragmento (dict): fragmento que guarda el nodo.

        Returns:
            None
        """
        self.clave = fragmento["codigo"]
        self.valor = fragmento
        self.izq = None
        self.der = None


class ArbolBinarioBusqueda:
    """Árbol binario de búsqueda propio.

    Insertar y buscar son iterativos: con claves ordenadas el árbol se degenera
    y una versión recursiva superaría el límite de recursión de Python.
    """

    def __init__(self):
        """Crea un árbol vacío.

        Returns:
            None
        """
        self.raiz = None
        self.tamano = 0

    def insertar(self, fragmento):
        """Inserta un fragmento por su código; si la clave existe, actualiza su valor.

        Args:
            fragmento (dict): fragmento con la clave 'codigo'.

        Returns:
            bool: True si se insertó un nodo nuevo, False si la clave ya existía.
        """
        nuevo = NodoArbol(fragmento)
        if self.raiz is None:
            self.raiz, self.tamano = nuevo, 1
            return True
        actual = self.raiz
        while True:
            if nuevo.clave == actual.clave:
                actual.valor = fragmento
                return False
            if nuevo.clave < actual.clave:
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
        actual, comparaciones = self.raiz, 0
        while actual is not None:
            comparaciones += 1
            if codigo == actual.clave:
                return actual.valor, comparaciones
            actual = actual.izq if codigo < actual.clave else actual.der
        return None, comparaciones

    def preorden(self):
        """Recorre el árbol en preorden (raíz, izquierda, derecha).

        Returns:
            list: fragmentos en el orden del recorrido.
        """
        res = []

        def r(n):
            if n:
                res.append(n.valor)
                r(n.izq)
                r(n.der)
        r(self.raiz)
        return res

    def inorden(self):
        """Recorre el árbol en inorden (izquierda, raíz, derecha): claves ordenadas.

        Returns:
            list: fragmentos en el orden del recorrido.
        """
        res = []

        def r(n):
            if n:
                r(n.izq)
                res.append(n.valor)
                r(n.der)
        r(self.raiz)
        return res

    def postorden(self):
        """Recorre el árbol en postorden (izquierda, derecha, raíz).

        Returns:
            list: fragmentos en el orden del recorrido.
        """
        res = []

        def r(n):
            if n:
                r(n.izq)
                r(n.der)
                res.append(n.valor)
        r(self.raiz)
        return res

    def por_niveles(self):
        """Recorre el árbol por niveles usando una cola (deque).

        Returns:
            list: fragmentos nivel por nivel.
        """
        res, cola = [], deque([self.raiz] if self.raiz else [])
        while cola:
            n = cola.popleft()
            res.append(n.valor)
            if n.izq:
                cola.append(n.izq)
            if n.der:
                cola.append(n.der)
        return res

    def altura(self):
        """Calcula la altura del árbol (nodos del camino más largo).

        Returns:
            int: altura; 0 si el árbol está vacío.
        """
        cola, altura = deque([(self.raiz, 1)] if self.raiz else []), 0
        while cola:
            nodo, altura = cola.popleft()
            cola.extend((h, altura + 1) for h in (nodo.izq, nodo.der) if h)
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
    """Verifica que los fragmentos estén ordenados por código (estrictamente crecientes).

    Args:
        fragmentos (list): fragmentos a verificar.

    Returns:
        bool: True si cada código es menor que el siguiente.
    """
    codigos = [f["codigo"] for f in fragmentos]
    return all(a < b for a, b in zip(codigos, codigos[1:]))


def comparar_busquedas(tamano, ordenado=False):
    """Compara el promedio de comparaciones entre el árbol y la búsqueda secuencial.

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
    total_arbol = sum(arbol.buscar(c)[1] for c in codigos)
    total_sec = sum(buscar_secuencial(lista, c)[1] for c in codigos)
    return {
        "tamano": tamano,
        "altura": arbol.altura(),
        "promedio_arbol": total_arbol / tamano,
        "promedio_secuencial": total_sec / tamano,
    }