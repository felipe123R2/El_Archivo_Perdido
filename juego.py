"""
Módulo Principal - El Archivo Perdido
Controla la narrativa, interacción con el usuario, recorrido de las salas 1 a 5,
preguntas conceptuales y persistencia de partida.
"""

import sys
import estructuras
import persistencia


def leer_entero(mensaje):
    """Valida que la entrada del usuario sea un número entero válido."""
    while True:
        entrada = input(mensaje)
        try:
            return int(entrada)
        except ValueError:
            print("❌ Entrada no válida. Ingrese un número entero.")


def leer_texto(mensaje):
    """Valida que la cadena ingresada por el usuario no esté vacía."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("❌ El texto no puede estar vacío.")


def hacer_pregunta_conceptual(pregunta, opciones, respuesta_correcta, pista):
    """Muestra la pregunta teórica al final de cada sala con opción de reintento."""
    print("\n--- Reto Teórico de la Sala ---")
    print(pregunta)
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")

    while True:
        res = leer_entero("\nSeleccione su respuesta (número): ")
        if res == respuesta_correcta:
            print("✅ ¡Correcto! Ha comprendido la estructura de datos.")
            return True
        else:
            print(f"❌ Respuesta incorrecta. Retroalimentación: {pista}")
            print("Inténtelo nuevamente...")


def sala_vestibulo(jugador):
    """Sala 1: Vestíbulo - Registro y validación de variables de entrada."""
    print("\n" + "=" * 50)
    print("      SALA 1: VESTÍBULO (Variables y Tipos)")
    print("=" * 50)
    print(
        "Bienvenido a la biblioteca. Inicializando los atributos del explorador..."
    )

    jugador["vida"] = 100
    jugador["puntaje"] = 0
    jugador["nivel"] = 1
    jugador["activo"] = True

    print(
        f"\n[OK] Atributos registrados: Nombre={jugador['nombre']} (str), Vida={jugador['vida']} (int), Puntaje={jugador['puntaje']} (int), Nivel={jugador['nivel']} (int)"
    )

    hacer_pregunta_conceptual(
        "¿Por qué es necesario validar el tipo de dato ingresado por el usuario?",
        [
            "Para evitar errores en ejecuciones numéricas o incompatibilidad de tipos.",
            "Porque Python obliga a definir tipos estáticos en todas las variables.",
            "Para que las variables ocupen el doble de memoria.",
        ],
        respuesta_correcta=1,
        pista="Recuerde que leer texto cuando se espera un número genera un ValueError al operar.",
    )

    frag = estructuras.crear_fragmento_diccionario(
        101, "Manual del Archivo", "Vestíbulo", 40
    )
    return frag


def sala_estanterias(inventario):
    """Sala 2: Estanterías - Gestión de Listas e inventario."""
    print("\n" + "=" * 50)
    print("      SALA 2: ESTANTERÍAS (Listas)")
    print("=" * 50)
    print(
        "Recorriendo los pasillos. Agregando y organizando fragmentos en la lista..."
    )

    frag = estructuras.crear_fragmento_diccionario(
        102, "Índice General de Secciones", "Estanterías", 80
    )
    estructuras.agregar_fragmento(inventario, frag)
    print(f"-> Fragmento recuperado: {frag['titulo']}")

    estructuras.ordenar_inventario_por_valor(inventario)
    valiosos = estructuras.obtener_fragmentos_valiosos(inventario, umbral=50)
    print(
        f"-> Comprensión de listas aplicada. Fragmentos valiosos (>=50 pts): {len(valiosos)}"
    )

    hacer_pregunta_conceptual(
        "¿Qué propiedad define a una Lista en Python?",
        [
            "Es una estructura inmutable cuyos elementos no se pueden modificar.",
            "Es una colección secuencial mutable que permite insertar, eliminar y ordenar.",
            "Es una estructura que no permite elementos duplicados.",
        ],
        respuesta_correcta=2,
        pista="Piense en las operaciones de agregar y ordenar que acabamos de realizar en el inventario.",
    )

    return frag


def sala_mapas(inventario):
    """Sala 3: Mapas - Coordenadas inmutables y Tuplas."""
    print("\n" + "=" * 50)
    print("      SALA 3: MAPAS (Tuplas)")
    print("=" * 50)
    print("Localizando la ubicación física de los archivos mediante tuplas...")

    pos = estructuras.crear_posicion(3, 12)
    pos_texto = estructuras.desempaquetar_posicion(pos)
    print(f"-> Coordenada fija generada (tupla): {pos} | {pos_texto}")

    frag = estructuras.crear_fragmento_diccionario(
        103, "Plano Antiguo de la Galería", "Mapas", 60
    )
    frag["posicion"] = pos
    estructuras.agregar_fragmento(inventario, frag)

    hacer_pregunta_conceptual(
        "¿Por qué se utilizan tuplas para representar posiciones o coordenadas fijas?",
        [
            "Porque son inmutables y evitan alteraciones accidentales de los datos.",
            "Porque permiten modificar sus valores dinámicamente durante la ejecución.",
            "Porque convierten automáticamente los números a texto.",
        ],
        respuesta_correcta=1,
        pista="La inmutabilidad de la tupla asegura que la posición (estante, nivel) no cambie por error.",
    )

    return frag


def sala_fichas(inventario):
    """Sala 4: Fichas - Campos y Diccionarios."""
    print("\n" + "=" * 50)
    print("      SALA 4: FICHAS (Diccionarios)")
    print("=" * 50)
    print(
        "Consultando el catálogo detallado del fragmento usando clave-valor..."
    )

    frag = estructuras.crear_fragmento_diccionario(
        104, "Ficha de Registro Histórico", "Fichas", 90
    )
    estructuras.agregar_fragmento(inventario, frag)

    print(
        f"-> Código: {estructuras.consultar_campo_fragmento(frag, 'codigo')}"
    )
    print(
        f"-> Título: {estructuras.consultar_campo_fragmento(frag, 'titulo')}"
    )
    print(
        f"-> Consulta de campo inexistente: {estructuras.consultar_campo_fragmento(frag, 'ubicacion_secreta')}"
    )

    hacer_pregunta_conceptual(
        "¿Qué beneficio principal brinda un Diccionario frente a una lista simple?",
        [
            "Acceso explícito mediante claves descriptivas sin depender de índices numéricos.",
            "Garantiza que el orden de los datos sea inmutable.",
            "Impide almacenar valores repetidos.",
        ],
        respuesta_correcta=1,
        pista="Es más claro acceder mediante una clave como 'titulo' que recordar el índice numérico [1].",
    )

    return frag


def sala_sellos(inventario):
    """Sala 5: Sellos - Validación de duplicados y Conjuntos."""
    print("\n" + "=" * 50)
    print("      SALA 5: SELLOS (Conjuntos / Sets)")
    print("=" * 50)
    print("Depurando códigos duplicados y comparando pistas...")

    codigos_muestra = [101, 102, 103, 101, 104, 102, 105]
    unicos = estructuras.detectar_y_eliminar_duplicados(codigos_muestra)
    print(f"-> Lista de códigos recibida: {codigos_muestra}")
    print(f"-> Códigos depurados con set (unicidad): {unicos}")

    pistas_req = {"Sello Oficial", "Tinta Roja", "Firma"}
    pistas_jug = {"Sello Oficial", "Firma", "Llave"}
    coincidencias, faltantes = estructuras.comparar_pistas_conjuntos(
        pistas_req, pistas_jug
    )
    print(
        f"-> Pistas validadas (intersección): {coincidencias} | Faltantes (diferencia): {faltantes}"
    )

    frag = estructuras.crear_fragmento_diccionario(
        105, "Sello de Autenticación", "Sellos", 95
    )
    estructuras.agregar_fragmento(inventario, frag)

    hacer_pregunta_conceptual(
        "¿Cuál es una propiedad fundamental de los Conjuntos (sets) en Python?",
        [
            "Permiten elementos duplicados siempre que sean enteros.",
            "No contienen elementos duplicados y admiten operaciones de teoría de conjuntos.",
            "Mantienen siempre los elementos ordenados según su inserción.",
        ],
        respuesta_correcta=2,
        pista="Al convertir a conjunto se eliminaron automáticamente los códigos repetidos.",
    )

    return frag


def menu_juego():
    """Menu principal de consola y control del recorrido."""
    jugador = {"nombre": "", "vida": 0, "puntaje": 0, "nivel": 0, "activo": False}
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
            break
        elif opcion == 2:
            datos = persistencia.cargar_partida()
            if datos:
                jugador = datos.get("jugador", jugador)
                inventario = datos.get("inventario", [])
                sala_actual = datos.get("sala_actual", 1)
                print(
                    f"\n¡Bienvenido de nuevo, {jugador['nombre']}! Reanudando en Sala {sala_actual}..."
                )
                break
        elif opcion == 3:
            persistencia.mostrar_ranking()
        elif opcion == 4:
            print("Saliendo del juego...")
            sys.exit(0)
        else:
            print("❌ Opción inválida.")

    # Ejecución secuencial de salas 1 a 5
    if sala_actual <= 1:
        f1 = sala_vestibulo(jugador)
        estructuras.agregar_fragmento(inventario, f1)
        jugador["puntaje"] += 50
        sala_actual = 2
        persistencia.guardar_partida(jugador, inventario, sala_actual)

    if sala_actual == 2:
        sala_estanterias(inventario)
        jugador["puntaje"] += 50
        sala_actual = 3
        persistencia.guardar_partida(jugador, inventario, sala_actual)

    if sala_actual == 3:
        sala_mapas(inventario)
        jugador["puntaje"] += 50
        sala_actual = 4
        persistencia.guardar_partida(jugador, inventario, sala_actual)

    if sala_actual == 4:
        sala_fichas(inventario)
        jugador["puntaje"] += 50
        sala_actual = 5
        persistencia.guardar_partida(jugador, inventario, sala_actual)

    if sala_actual == 5:
        sala_sellos(inventario)
        jugador["puntaje"] += 50
        sala_actual = 6
        persistencia.guardar_partida(jugador, inventario, sala_actual)

    print("\n" + "=" * 50)
    print(" 🎉 ¡RECORRIDO COMPLETADO (SALAS 1 A 5)!")
    print("=" * 50)
    print(f"Explorador: {jugador['nombre']}")
    print(f"Puntaje total: {jugador['puntaje']} pts")
    print(f"Fragmentos recolectados en el inventario: {len(inventario)}")

    persistencia.guardar_puntaje(jugador["nombre"], jugador["puntaje"])
    print(
        "\n✅ Avance registrado correctamente en la tabla de posiciones y archivos JSON."
    )


if __name__ == "__main__":
    menu_juego()