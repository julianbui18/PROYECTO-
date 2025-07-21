import random
import time

def crear_tablero(numero_filas, numero_columnas):
    return [["■" for _ in range(numero_columnas)] for _ in range(numero_filas)]

def colocar_minas(tablero, cantidad_minas):
    minas_colocadas = 0
    while minas_colocadas < cantidad_minas:
        fila = random.randint(0, len(tablero) - 1)
        columna = random.randint(0, len(tablero[0]) - 1)
        if tablero[fila][columna] != "*":
            tablero[fila][columna] = "*"
            minas_colocadas += 1

def contar_minas_de_alrededor(tablero, fila, columna):
    minas = 0
    for fila_actual in range(fila - 1, fila + 2):
        for columna_actual in range(columna - 1, columna + 2):
            if 0 <= fila_actual < len(tablero) and 0 <= columna_actual < len(tablero[0]):
                if tablero[fila_actual][columna_actual] == "*":
                    minas += 1
    return minas

def descubrir(tablero_visible, tablero_oculto, fila, columna):
    if tablero_visible[fila][columna] == "B":
        return
    if tablero_oculto[fila][columna] == "*":
        tablero_visible[fila][columna] = "*"
        return
    minas_cerca = contar_minas_de_alrededor(tablero_oculto, fila, columna)
    if minas_cerca > 0:
        tablero_visible[fila][columna] = str(minas_cerca)
    else:
        tablero_visible[fila][columna] = "."
        for fila_vecina in range(fila - 1, fila + 2):
            for columna_vecina in range(columna - 1, columna + 2):
                if 0 <= fila_vecina < len(tablero_visible) and 0 <= columna_vecina < len(tablero_visible[0]):
                    if tablero_visible[fila_vecina][columna_vecina] == "■":
                        descubrir(tablero_visible, tablero_oculto, fila_vecina, columna_vecina)

def mostrar(tablero):
    print("   " + " ".join(str(numero) for numero in range(len(tablero[0]))))
    for indice_fila, fila in enumerate(tablero):
        print(str(indice_fila).rjust(2), " ".join(fila))

def revisar_si_gano(tablero_visible, tablero_oculto):
    for fila in range(len(tablero_visible)):
        for columna in range(len(tablero_visible[0])):
            if tablero_visible[fila][columna] == "■" and tablero_oculto[fila][columna] != "*":
                return False
    return True

def jugar():
    print("Bienvenido a Buscaminas")
    print("1. Facil (5x5, 3 minas)")
    print("2. Pro (8x8, 10 minas)")
    print("3. Pro max (10x10, 20 minas)")

    nivel = input("Selecciona dificultad (1, 2, 3): ")
    if nivel == "1":
        numero_filas, numero_columnas, cantidad_minas = 5, 5, 3
    elif nivel == "2":
        numero_filas, numero_columnas, cantidad_minas = 8, 8, 10
    elif nivel == "3":
        numero_filas, numero_columnas, cantidad_minas = 10, 10, 20
    else:
        print("Opción inválida. Se usará fácil por defecto.")
        numero_filas, numero_columnas, cantidad_minas = 5, 5, 3

    tablero_visible = crear_tablero(numero_filas, numero_columnas)
    tablero_oculto = crear_tablero(numero_filas, numero_columnas)
    colocar_minas(tablero_oculto, cantidad_minas)

    inicio = time.time()
    juego_terminado = False

    while not juego_terminado:
        mostrar(tablero_visible)
        print("Para descubrir: fila columna (ej. 2 3)")
        print("Para bandera: b fila columna (ej. b 2 3)")
        entrada = input("Tu jugada: ").split()

        if not entrada:
            continue

        if entrada[0] == "b" and len(entrada) == 3:
            fila = int(entrada[1])
            columna = int(entrada[2])
            if tablero_visible[fila][columna] == "■":
                tablero_visible[fila][columna] = "B"
            elif tablero_visible[fila][columna] == "B":
                tablero_visible[fila][columna] = "■"

        elif len(entrada) == 2:
            fila = int(entrada[0])
            columna = int(entrada[1])
            if tablero_visible[fila][columna] == "B":
                continue

            if tablero_oculto[fila][columna] == "*":
                tablero_visible[fila][columna] = "*"
                mostrar(tablero_visible)
                print("¡Perdiste!")
                juego_terminado = True

            else:
                descubrir(tablero_visible, tablero_oculto, fila, columna)
                if revisar_si_gano(tablero_visible, tablero_oculto):
                    mostrar(tablero_visible)
                    print("¡Ganaste!")
                    juego_terminado = True

    fin = time.time()
    duracion = round(fin - inicio, 2)
    print(f"Tiempo total: {duracion} segundos")
    input("Presiona Enter para salir...")

jugar()