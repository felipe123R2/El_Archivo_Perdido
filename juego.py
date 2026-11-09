"""
Módulo Principal - El Archivo Perdido
Controla la narrativa, la interacción con el usuario, el recorrido de las
salas 1 a 5, la Sala Central (reconstrucción del catálogo) y la persistencia.
"""

import sys
import estructuras
import persistencia

SALA_CENTRAL = 6
PARTIDA_TERMINADA = 7


# ---------------------------------------------------------------- entradas
def leer_entero(mensaje):
    """Lee un número entero validando la entrada.

    Args:
        mensaje (str): texto que se muestra al usuario.

    Returns:
        int: el número ingresado.
    """
    while True:
        entrada = input(mensaje)
        try:
            return int(entrada)
        except ValueError:
            print("❌ Entrada no válida. Ingrese un número entero.")


def leer_flotante(mensaje):
    """Lee un número decimal no negativo validando la entrada.

    Args:
        mensaje (str): texto que se muestra al usuario.

    Returns:
        float: el número ingresado.
    """
    while True:
        entrada = input(mensaje).replace(",", ".")
        try:
            valor = float(entrada)
            if valor >= 0:
                return valor
            print("❌ El valor no puede ser negativo.")
        except ValueError:
            print("❌ Entrada no válida. Ingrese un número (ej. 1.5).")


def leer_texto(mensaje):
    """Lee una cadena no vacía.

    Args:
        mensaje (str): texto que se muestra al usuario.

    Returns:
        str: texto ingresado sin espacios en los extremos.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("❌ El texto no puede estar vacío.")


# ---------------------------------------------------------------- utilidades
def hacer_pregunta_conceptual(jugador, pregunta, opciones, respuesta_correcta, pista):
    """Plantea la pregunta teórica de la sala, con pista y reintento.

    Cada error resta 5 puntos de vida (mínimo 1).

    Args:
        jugador (dict): atributos del jugador.
        pregunta (str): enunciado.
        opciones (list): textos de las opciones.
        respuesta_correcta (int): número (desde 1) de la opción correcta.
        pista (str): retroalimentación ante un error.

    Returns:
        int: número de intentos empleados.
    """
    print("\n--- Reto Teórico de la Sala ---")
    print(pregunta)
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")

    intentos = 0
    while True:
        res = leer_entero("\nSeleccione su respuesta (número): ")
        intentos += 1
        if res == respuesta_correcta:
            print("✅ ¡Correcto! Ha comprendido la estructura de datos.")
            return intentos
        jugador["vida"] = max(1, jugador["vida"] - 5)
        print(f"❌ Respuesta incorrecta (vida: {jugador['vida']}). Pista: {pista}")
        print("Inténtelo nuevamente...")


def otorgar_puntos(jugador, intentos, siguiente_sala):
    """Suma los puntos de una sala según los intentos y el multiplicador.

    Args:
        jugador (dict): atributos del jugador.
        intentos (int): intentos usados en la pregunta conceptual.
        siguiente_sala (int): número de la sala que se desbloquea.

    Returns:
        int: puntos obtenidos en la sala.
    """
    base = max(10, 50 - 10 * (intentos - 1))
    mult = jugador["multiplicador"]
    puntos = int(round(base * mult))
    jugador["puntaje"] += puntos
    jugador["nivel"] = min(siguiente_sala, SALA_CENTRAL)
    jugador["multiplicador"] = round(mult + 0.1, 1)
    print(
        f"\n⭐ +{puntos} pts (x{mult:.1f}) | "
        f"Puntaje: {jugador['puntaje']} | Vida: {jugador['vida']} | Nivel: {jugador['nivel']}"
    )
    return puntos


def mostrar_inventario(inventario):
    """Muestra el inventario de fragmentos.

    Args:
        inventario (list): fragmentos recolectados.

    Returns:
        None
    """
    print("\n--- INVENTARIO ---")
    if not inventario:
        print("(vacío)")
    for f in inventario:
        print(f"  [{f['codigo']}] {f['titulo']} ({f['sala']}) - {f['valor']} pts")
    print(f"Total: {len(inventario)} fragmento(s)")


def mostrar_instrucciones():
    """Muestra las reglas del juego.

    Returns:
        None
    """
    print("\n--- INSTRUCCIONES ---")
    print("La biblioteca perdió su catálogo. Recorra cinco salas, recupere un")
    print("fragmento en cada una y responda la pregunta conceptual. Un error")
    print("resta vida y puntos; al final reconstruirá el catálogo en la Sala Central.")
    print("Su avance se guarda automáticamente al terminar cada sala.")


# ---------------------------------------------------------------- salas
def sala_vestibulo(jugador, inventario):
    """Sala 1: Vestíbulo - variables, tipos y validación de entradas.

    Args:
        jugador (dict): atributos del jugador (se inicializan aquí).
        inventario (list): inventario donde se agrega el fragmento.

    Returns:
        int: intentos usados en la pregunta conceptual.
    """
    print("\n" + "=" * 50)
    print("      SALA 1: VESTÍBULO (Variables y Tipos)")
    print("=" * 50)
    print("Bienvenido a la biblioteca. Inicializando los atributos del explorador...")

    jugador["experiencia"] = leer_flotante(
        "¿Cuántos años de experiencia programando tiene? (ej. 1.5): "
    )
    jugador["vida"] = 100
    jugador["puntaje"] = 0
    jugador["nivel"] = 1
    jugador["multiplicador"] = 1.0
    jugador["activo"] = True

    print(
        f"\n[OK] Nombre={jugador['nombre']} ({type(jugador['nombre']).__name__}), "
        f"Vida={jugador['vida']} ({type(jugador['vida']).__name__}), "
        f"Experiencia={jugador['experiencia']} ({type(jugador['experiencia']).__name__}), "
        f"Activo={jugador['activo']} ({type(jugador['activo']).__name__})"
    )

    intentos = hacer_pregunta_conceptual(
        jugador,
        "¿Por qué es necesario validar el tipo de dato ingresado por el usuario?",
        [
            "Para evitar errores en ejecuciones numéricas o incompatibilidad de tipos.",
            "Porque Python obliga a definir tipos estáticos en todas las variables.",
            "Para que las variables ocupen el doble de memoria.",
        ],
        respuesta_correcta=1,
        pista="Leer texto cuando se espera un número genera un ValueError al operar.",
    )
    estructuras.agregar_fragmento(
        inventario,
        estructuras.crear_fragmento_diccionario(101, "Manual del Archivo", "Vestíbulo", 40),
    )
    return intentos


def sala_estanterias(jugador, inventario):
    """Sala 2: Estanterías - inserción, búsqueda, eliminación y orden en listas.

    Args:
        jugador (dict): atributos del jugador.
        inventario (list): inventario de fragmentos.

    Returns:
        int: intentos usados en la pregunta conceptual.
    """
    print("\n" + "=" * 50)
    print("      SALA 2: ESTANTERÍAS (Listas)")
    print("=" * 50)
    print("Recorriendo los pasillos. Agregando y organizando fragmentos en la lista...")

    frag = estructuras.crear_fragmento_diccionario(
        102, "Índice General de Secciones", "Estanterías", 80
    )
    estructuras.agregar_fragmento(inventario, frag)
    print(f"-> Fragmento recuperado: {frag['titulo']}")

    # Inserción, búsqueda y eliminación de una hoja dañada
    danada = estructuras.crear_fragmento_diccionario(199, "Hoja Dañada", "Estanterías", 0)
    estructuras.agregar_fragmento(inventario, danada)
    hallada = estructuras.buscar_fragmento_lista(inventario, 199)
    print(f"-> Búsqueda por código 199: {hallada['titulo'] if hallada else 'no encontrada'}")
    if estructuras.eliminar_fragmento(inventario, 199):
        print("-> La hoja dañada no sirve y fue eliminada del inventario.")

    estructuras.ordenar_inventario_por_valor(inventario)
    valiosos = estructuras.obtener_fragmentos_valiosos(inventario, umbral=50)
    print(f"-> Inventario ordenado por valor. Fragmentos valiosos (>=50 pts): {len(valiosos)}")

    return hacer_pregunta_conceptual(
        jugador,
        "¿Qué propiedad define a una Lista en Python?",
        [
            "Es una estructura inmutable cuyos elementos no se pueden modificar.",
            "Es una colección secuencial mutable que permite insertar, eliminar y ordenar.",
            "Es una estructura que no permite elementos duplicados.",
        ],
        respuesta_correcta=2,
        pista="Piense en las operaciones de agregar, eliminar y ordenar que acabamos de hacer.",
    )


def sala_mapas(jugador, inventario):
    """Sala 3: Mapas - tuplas inmutables y desempaquetado en un recorrido.

    Args:
        jugador (dict): atributos del jugador.
        inventario (list): inventario de fragmentos.

    Returns:
        int: intentos usados en la pregunta conceptual.
    """
    print("\n" + "=" * 50)
    print("      SALA 3: MAPAS (Tuplas)")
    print("=" * 50)
    print("Localizando la ubicación física de los archivos mediante tuplas...")

    ruta = [
        estructuras.crear_posicion(1, 1),
        estructuras.crear_posicion(2, 4),
        estructuras.crear_posicion(3, 12),
    ]
    print("-> Recorrido por la galería:")
    for paso, pos in enumerate(ruta, 1):
        print(f"   Paso {paso}: {pos} -> {estructuras.desempaquetar_posicion(pos)}")
    pos = ruta[-1]

    try:
        pos[0] = 99
    except TypeError:
        print("-> Intento de modificar la tupla rechazado: las tuplas son inmutables.")

    frag = estructuras.crear_fragmento_diccionario(
        103, "Plano Antiguo de la Galería", "Mapas", 60
    )
    frag["posicion"] = pos
    estructuras.agregar_fragmento(inventario, frag)

    return hacer_pregunta_conceptual(
        jugador,
        "¿Por qué se utilizan tuplas para representar posiciones o coordenadas fijas?",
        [
            "Porque son inmutables y evitan alteraciones accidentales de los datos.",
            "Porque permiten modificar sus valores dinámicamente durante la ejecución.",
            "Porque convierten automáticamente los números a texto.",
        ],
        respuesta_correcta=1,
        pista="La inmutabilidad asegura que la posición (estante, nivel) no cambie por error.",
    )


def sala_fichas(jugador, inventario):
    """Sala 4: Fichas - diccionarios, consultas por clave y claves inexistentes.

    Args:
        jugador (dict): atributos del jugador.
        inventario (list): inventario de fragmentos.

    Returns:
        int: intentos usados en la pregunta conceptual.
    """
    print("\n" + "=" * 50)
    print("      SALA 4: FICHAS (Diccionarios)")
    print("=" * 50)
    print("Consultando el catálogo detallado del fragmento usando clave-valor...")

    frag = estructuras.crear_fragmento_diccionario(
        104, "Ficha de Registro Histórico", "Fichas", 90
    )
    estructuras.agregar_fragmento(inventario, frag)

    print(f"-> Código: {estructuras.consultar_campo_fragmento(frag, 'codigo')}")
    print(f"-> Título: {estructuras.consultar_campo_fragmento(frag, 'titulo')}")
    print(f"-> Clave inexistente: {estructuras.consultar_campo_fragmento(frag, 'ubicacion_secreta')}")

    return hacer_pregunta_conceptual(
        jugador,
        "¿Qué beneficio principal brinda un Diccionario frente a una lista simple?",
        [
            "Acceso explícito mediante claves descriptivas sin depender de índices numéricos.",
            "Garantiza que el orden de los datos sea inmutable.",
            "Impide almacenar valores repetidos.",
        ],
        respuesta_correcta=1,
        pista="Es más claro acceder con una clave como 'titulo' que recordar el índice [1].",
    )


def sala_sellos(jugador, inventario):
    """Sala 5: Sellos - conjuntos: duplicados reales y validación de pistas.

    Se halla una copia repetida del fragmento 101; se detecta con un
    conjunto y se descartará en la Sala Central.

    Args:
        jugador (dict): atributos del jugador.
        inventario (list): inventario de fragmentos.

    Returns:
        int: intentos usados en la pregunta conceptual.
    """
    print("\n" + "=" * 50)
    print("      SALA 5: SELLOS (Conjuntos / Sets)")
    print("=" * 50)
    print("Depurando códigos duplicados y comparando pistas...")

    estructuras.agregar_fragmento(
        inventario,
        estructuras.crear_fragmento_diccionario(105, "Sello de Autenticación", "Sellos", 95),
    )
    # Una caja sellada contiene una copia repetida del Manual del Archivo
    copia = estructuras.buscar_fragmento_lista(inventario, 101)
    if copia:
        estructuras.agregar_fragmento(inventario, dict(copia))

    codigos = [f["codigo"] for f in inventario]
    unicos = estructuras.detectar_y_eliminar_duplicados(codigos)
    repetidos = estructuras.codigos_duplicados(codigos)
    print(f"-> Códigos en el inventario: {codigos}")
    print(f"-> Códigos únicos (set): {sorted(unicos)} | Repetidos: {sorted(repetidos)}")

    pistas_req = {"Sello Oficial", "Tinta Roja", "Firma"}
    pistas_jug = {"Sello Oficial", "Firma", "Llave"}
    coincidencias, faltantes = estructuras.comparar_pistas_conjuntos(pistas_req, pistas_jug)
    todas = pistas_req.union(pistas_jug)
    print(f"-> Validadas (intersección): {sorted(coincidencias)}")
    print(f"-> Faltantes (diferencia): {sorted(faltantes)}")
    print(f"-> Todas las pistas conocidas (unión): {sorted(todas)}")

    return hacer_pregunta_conceptual(
        jugador,
        "¿Cuál es una propiedad fundamental de los Conjuntos (sets) en Python?",
        [
            "Permiten elementos duplicados siempre que sean enteros.",
            "No contienen elementos duplicados y admiten operaciones de teoría de conjuntos.",
            "Mantienen siempre los elementos ordenados según su inserción.",
        ],
        respuesta_correcta=2,
        pista="Al convertir a conjunto se eliminaron automáticamente los códigos repetidos.",
    )


def mostrar_tabla_comparativa():
    """Muestra la comparación árbol vs. búsqueda secuencial para varios tamaños.

    Returns:
        None
    """
    print("\n--- Comparaciones promedio por búsqueda ---")
    print(f"{'Tamaño':>7} | {'Inserción':<10} | {'Altura':>6} | {'Árbol':>8} | {'Secuencial':>10}")
    for n in (10, 100, 1000):
        for ordenado in (False, True):
            r = estructuras.comparar_busquedas(n, ordenado)
            tipo = "ordenada" if ordenado else "aleatoria"
            print(
                f"{n:>7} | {tipo:<10} | {r['altura']:>6} | "
                f"{r['promedio_arbol']:>8.1f} | {r['promedio_secuencial']:>10.1f}"
            )
    print("Con inserciones ordenadas el árbol se degenera y se comporta como una lista.")


def sala_central(jugador, inventario):
    """Sala Central: La Reconstrucción del Catálogo (pasos 1 a 6).

    Args:
        jugador (dict): atributos del jugador (se actualiza el puntaje).
        inventario (list): fragmentos recolectados.

    Returns:
        None
    """
    print("\n" + "=" * 50)
    print("      SALA CENTRAL: RECONSTRUCCIÓN DEL CATÁLOGO")
    print("=" * 50)

    # Paso 1: carga desde archivo
    print("\n[Paso 1] Carga desde archivo")
    persistencia.guardar_fragmentos(inventario)
    fragmentos = persistencia.cargar_fragmentos()
    if fragmentos is None:
        print("-> Se usará el inventario en memoria.")
        fragmentos = [dict(f) for f in inventario]
    print(f"-> Fragmentos leídos: {len(fragmentos)}")

    # Paso 2: depuración con conjunto de códigos
    print("\n[Paso 2] Depuración de duplicados")
    fragmentos, descartados = estructuras.depurar_fragmentos(fragmentos)
    print(f"-> Fragmentos descartados: {descartados} | Válidos: {len(fragmentos)}")

    # Paso 3: ubicación con tuplas
    print("\n[Paso 3] Ubicación en la biblioteca")
    for f in fragmentos:
        pos = estructuras.asignar_posicion(f)
        print(f"-> [{f['codigo']}] {f['titulo']}: {estructuras.desempaquetar_posicion(pos)}")

    # Paso 4: construcción del árbol
    print("\n[Paso 4] Construcción del árbol binario de búsqueda")
    arbol = estructuras.ArbolBinarioBusqueda()
    for f in fragmentos:
        arbol.insertar(f)
    print(f"-> Nodos: {arbol.tamano} | Altura: {arbol.altura()}")

    # Paso 5: verificación inorden
    print("\n[Paso 5] Verificación con recorrido inorden")
    ordenados = arbol.inorden()
    print(f"-> Inorden: {[f['codigo'] for f in ordenados]}")
    if estructuras.esta_ordenada(ordenados):
        print("✅ El catálogo está correctamente ordenado.")
    else:
        print("❌ ERROR: el recorrido inorden no está ordenado.")

    # Paso 6: consulta
    print("\n[Paso 6] Consulta de fragmentos")
    consultas_fallidas = 0
    while True:
        print("\n1. Buscar fragmento por código")
        print("2. Ver tabla comparativa (árbol vs. secuencial)")
        print("0. Terminar reconstrucción")
        op = leer_entero("Seleccione una opción: ")
        if op == 0:
            break
        elif op == 1:
            codigo = leer_entero("Código a buscar: ")
            frag, comp_arbol = arbol.buscar(codigo)
            _, comp_sec = estructuras.buscar_secuencial(fragmentos, codigo)
            if frag:
                print(f"✅ Encontrado: {frag['titulo']} ({estructuras.desempaquetar_posicion(frag['posicion'])})")
            else:
                consultas_fallidas += 1
                print("❌ No existe un fragmento con ese código.")
            print(f"   Comparaciones -> árbol: {comp_arbol} | secuencial: {comp_sec}")
        elif op == 2:
            mostrar_tabla_comparativa()
        else:
            print("❌ Opción inválida.")

    # Puntuación: fragmentos válidos e intentos fallidos
    puntos = len(fragmentos) * 20 + max(0, 30 - 5 * consultas_fallidas)
    jugador["puntaje"] += puntos
    print(f"\n⭐ Reconstrucción: +{puntos} pts ({len(fragmentos)} fragmentos válidos, "
          f"{consultas_fallidas} consulta(s) fallida(s))")

    hacer_pregunta_conceptual(
        jugador,
        "¿Qué devuelve el recorrido inorden de un árbol binario de búsqueda?",
        [
            "Los elementos en orden creciente de su clave.",
            "Los elementos en el orden en que fueron insertados.",
            "Los elementos en orden aleatorio.",
        ],
        respuesta_correcta=1,
        pista="Se visita izquierda, raíz y derecha: los menores siempre van primero.",
    )


# ---------------------------------------------------------------- menú
def menu_juego():
    """Menú principal de consola y control del recorrido.

    Returns:
        None
    """
    jugador = {
        "nombre": "", "vida": 0, "puntaje": 0, "nivel": 0,
        "multiplicador": 1.0, "activo": False,
    }
    inventario = []
    sala_actual = 1

    while True:
        print("\n" + "=" * 50)
        print("      EL ARCHIVO PERDIDO - JUEGO SERIO")
        print("=" * 50)
        print("1. Iniciar nueva partida")
        print("2. Cargar partida guardada")
        print("3. Ver tabla de puntajes")
        print("4. Salir")

        opcion = leer_entero("\nSeleccione una opción: ")

        if opcion == 1:
            jugador["nombre"] = leer_texto("\nIngrese el nombre del explorador: ")
            inventario = []
            sala_actual = 1
            mostrar_instrucciones()
            break
        elif opcion == 2:
            datos = persistencia.cargar_partida()
            if datos:
                jugador.update(datos["jugador"])
                inventario = datos["inventario"]
                sala_actual = datos["sala_actual"]
                if sala_actual >= PARTIDA_TERMINADA:
                    print(f"\n{jugador.get('nombre', '')}: esta partida ya fue completada.")
                    print(f"Puntaje final: {jugador['puntaje']} pts")
                    continue
                print(f"\n¡Bienvenido de nuevo, {jugador.get('nombre', '')}! Reanudando en Sala {sala_actual}...")
                break
        elif opcion == 3:
            persistencia.mostrar_ranking()
        elif opcion == 4:
            print("Saliendo del juego...")
            sys.exit(0)
        else:
            print("❌ Opción inválida.")

    salas = [
        (1, sala_vestibulo),
        (2, sala_estanterias),
        (3, sala_mapas),
        (4, sala_fichas),
        (5, sala_sellos),
    ]
    for numero, funcion in salas:
        if sala_actual == numero:
            intentos = funcion(jugador, inventario)
            otorgar_puntos(jugador, intentos, numero + 1)
            sala_actual = numero + 1
            persistencia.guardar_partida(jugador, inventario, sala_actual)
            mostrar_inventario(inventario)

    if sala_actual == SALA_CENTRAL:
        sala_central(jugador, inventario)
        sala_actual = PARTIDA_TERMINADA
        persistencia.guardar_partida(jugador, inventario, sala_actual)
        persistencia.guardar_puntaje(jugador["nombre"], jugador["puntaje"])

        print("\n" + "=" * 50)
        print(" 🎉 ¡CATÁLOGO RECONSTRUIDO!")
        print("=" * 50)
        print(f"Explorador: {jugador['nombre']}")
        print(f"Puntaje total: {jugador['puntaje']} pts | Vida: {jugador['vida']}")
        print("\n✅ Resultado guardado en la partida y en la tabla de puntajes.")


if __name__ == "__main__":
    try:
        menu_juego()
    except (EOFError, KeyboardInterrupt):
        print("\n\nJuego interrumpido. Su avance hasta la última sala completada fue guardado.")
