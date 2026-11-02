"""
Módulo de Persistencia - El Archivo Perdido
Guardado y carga de datos del juego en archivos JSON, con manejo de excepciones.
"""

import json
import os

ARCHIVO_PARTIDA = "partida_guardada.json"
ARCHIVO_RANKING = "tabla_puntajes.json"
ARCHIVO_FRAGMENTOS = "fragmentos_recolectados.json"


def _normalizar_inventario(inventario):
    """Convierte las posiciones guardadas como listas de nuevo en tuplas.

    JSON no tiene tuplas, por lo que al cargar se restaura la inmutabilidad.

    Args:
        inventario (list): fragmentos leídos del archivo.

    Returns:
        list: fragmentos válidos con 'posicion' como tupla cuando existe.
    """
    resultado = []
    for frag in inventario:
        if not isinstance(frag, dict) or "codigo" not in frag:
            continue
        if isinstance(frag.get("posicion"), list):
            frag["posicion"] = tuple(frag["posicion"])
        resultado.append(frag)
    return resultado


def guardar_partida(datos_jugador, inventario, sala_actual):
    """Guarda el estado del jugador y su inventario en un archivo JSON.

    Args:
        datos_jugador (dict): atributos del jugador.
        inventario (list): fragmentos recolectados.
        sala_actual (int): próxima sala a jugar.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    datos = {
        "jugador": datos_jugador,
        "inventario": inventario,
        "sala_actual": sala_actual,
    }
    try:
        with open(ARCHIVO_PARTIDA, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"Error al guardar los datos: {e}")
        return False


def cargar_partida():
    """Carga una partida guardada y valida su estructura.

    Returns:
        dict | None: datos con 'jugador', 'inventario' y 'sala_actual',
        o None si el archivo no existe o está dañado.
    """
    if not os.path.exists(ARCHIVO_PARTIDA):
        print("No se encontró ningún archivo de partida guardada.")
        return None
    try:
        with open(ARCHIVO_PARTIDA, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al leer la partida guardada: {e}")
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
    try:
        with open(ARCHIVO_FRAGMENTOS, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=4, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"Error al guardar los fragmentos: {e}")
        return False


def cargar_fragmentos():
    """Lee los fragmentos recolectados desde su archivo (Paso 1).

    Returns:
        list | None: fragmentos válidos, o None si no se pudo leer.
    """
    if not os.path.exists(ARCHIVO_FRAGMENTOS):
        print("No se encontró el archivo de fragmentos recolectados.")
        return None
    try:
        with open(ARCHIVO_FRAGMENTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al leer los fragmentos: {e}")
        return None
    if not isinstance(datos, list):
        print("El archivo de fragmentos está mal formado.")
        return None
    return _normalizar_inventario(datos)


def _leer_ranking():
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
    return [
        r for r in datos
        if isinstance(r, dict) and "nombre" in r and "puntaje" in r
    ]


def guardar_puntaje(nombre, puntaje):
    """Agrega el puntaje final del jugador a la tabla de posiciones.

    Args:
        nombre (str): nombre del jugador.
        puntaje (int): puntaje final.

    Returns:
        bool: True si se guardó correctamente, False si hubo error.
    """
    ranking = _leer_ranking()
    if ranking is None:
        ranking = []
    ranking.append({"nombre": nombre, "puntaje": puntaje})
    ranking.sort(key=lambda x: x["puntaje"], reverse=True)
    try:
        with open(ARCHIVO_RANKING, "w", encoding="utf-8") as f:
            json.dump(ranking, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error al guardar la tabla de puntajes: {e}")
        return False


def mostrar_ranking():
    """Muestra la tabla de puntajes en consola.

    Returns:
        None
    """
    ranking = _leer_ranking()
    if ranking is None:
        print("Error al cargar la tabla de puntajes.")
        return
    if not ranking:
        print("\n--- No hay puntajes registrados ---")
        return
    print("\n====== TABLA DE PUNTAJES ======")
    for i, reg in enumerate(ranking, 1):
        print(f"{i}. {reg['nombre']} - {reg['puntaje']} pts")
    print("================================")
