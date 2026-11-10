"""
Módulo de Persistencia - El Archivo Perdido
Guardado y carga de datos del juego en archivos JSON, con manejo de excepciones.
"""

import json
import os

ARCHIVO_PARTIDA = "partida_guardada.json"
ARCHIVO_RANKING = "tabla_puntajes.json"
ARCHIVO_FRAGMENTOS = "fragmentos_recolectados.json"


def _guardar_json(ruta, datos, mensaje):
    """Escribe datos en un archivo JSON controlando los errores.

    Args:
        ruta (str): archivo de destino.
        datos (object): datos a guardar.
        mensaje (str): texto que se muestra si falla la escritura.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"{mensaje}: {e}")
        return False


def _cargar_json(ruta, nombre):
    """Lee un archivo JSON controlando archivos inexistentes y datos dañados.

    Args:
        ruta (str): archivo a leer.
        nombre (str): descripción del contenido, para los mensajes de error.

    Returns:
        object | None: los datos leídos, o None si no se pudo leer.
    """
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo de {nombre}.")
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al leer {nombre}: {e}")
        return None


def _normalizar_inventario(inventario):
    """Descarta fragmentos inválidos y convierte las posiciones de lista a tupla.

    JSON no tiene tuplas, por lo que al cargar se restaura la inmutabilidad.

    Args:
        inventario (list): fragmentos leídos del archivo.

    Returns:
        list: fragmentos válidos con 'posicion' como tupla cuando existe.
    """
    validos = [f for f in inventario if isinstance(f, dict) and "codigo" in f]
    for frag in validos:
        if isinstance(frag.get("posicion"), list):
            frag["posicion"] = tuple(frag["posicion"])
    return validos


def guardar_partida(datos_jugador, inventario, sala_actual):
    """Guarda el estado del jugador y su inventario en un archivo JSON.

    Args:
        datos_jugador (dict): atributos del jugador.
        inventario (list): fragmentos recolectados.
        sala_actual (int): próxima sala a jugar.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    datos = {"jugador": datos_jugador, "inventario": inventario, "sala_actual": sala_actual}
    return _guardar_json(ARCHIVO_PARTIDA, datos, "Error al guardar los datos")


def cargar_partida():
    """Carga una partida guardada y valida su estructura.

    Returns:
        dict | None: datos con 'jugador', 'inventario' y 'sala_actual',
        o None si el archivo no existe o está dañado.
    """
    datos = _cargar_json(ARCHIVO_PARTIDA, "la partida guardada")
    if datos is None:
        return None
    if (
        not isinstance(datos, dict)
        or not isinstance(datos.get("jugador"), dict)
        or not isinstance(datos.get("inventario"), list)
        or not isinstance(datos.get("sala_actual"), int)
    ):
        print("El archivo de partida está incompleto o mal formado.")
        return None
    datos["inventario"] = _normalizar_inventario(datos["inventario"])
    return datos


def guardar_fragmentos(inventario):
    """Guarda los fragmentos recolectados para la Sala Central (Paso 1).

    Args:
        inventario (list): fragmentos (diccionarios) recolectados.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    return _guardar_json(ARCHIVO_FRAGMENTOS, inventario, "Error al guardar los fragmentos")


def cargar_fragmentos():
    """Lee los fragmentos recolectados desde su archivo (Paso 1).

    Returns:
        list | None: fragmentos válidos, o None si no se pudo leer.
    """
    datos = _cargar_json(ARCHIVO_FRAGMENTOS, "los fragmentos recolectados")
    if datos is None:
        return None
    if not isinstance(datos, list):
        print("El archivo de fragmentos está mal formado.")
        return None
    return _normalizar_inventario(datos)


def cargar_ranking():
    """Lee la tabla de puntajes del disco.

    Returns:
        list | None: registros válidos; lista vacía si el archivo no
        existe; None si está dañado.
    """
    if not os.path.exists(ARCHIVO_RANKING):
        return []
    try:
        with open(ARCHIVO_RANKING, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
    if not isinstance(datos, list):
        return None
    return [r for r in datos if isinstance(r, dict) and "nombre" in r and "puntaje" in r]


def guardar_puntaje(nombre, puntaje):
    """Agrega el puntaje final del jugador a la tabla de posiciones.

    Args:
        nombre (str): nombre del jugador.
        puntaje (int): puntaje final.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    ranking = cargar_ranking() or []
    ranking.append({"nombre": nombre, "puntaje": puntaje})
    ranking.sort(key=lambda x: x["puntaje"], reverse=True)
    return _guardar_json(ARCHIVO_RANKING, ranking, "Error al guardar la tabla de puntajes")


def mostrar_ranking():
    """Muestra la tabla de puntajes en consola.

    Returns:
        None
    """
    ranking = cargar_ranking()
    if ranking is None:
        print("Error al cargar la tabla de puntajes.")
    elif not ranking:
        print("\n--- No hay puntajes registrados ---")
    else:
        print("\n====== TABLA DE PUNTAJES ======")
        for i, reg in enumerate(ranking, 1):
            print(f"{i}. {reg['nombre']} - {reg['puntaje']} pts")
        print("================================")