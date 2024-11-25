import pygame
import sys
import random
from .constants import *

import random
import json
import os


# Función para pedir el nombre del jugador
def pedir_nombre(pantalla, fuente):
    nombre = ""
    ingresando = True

    # Fuentes
    fuente = pygame.font.Font(None, 48)

    while ingresando:
        # Color de fondo
        pantalla.fill(COLOR_FONDO)

        # Mensaje de instrucción
        mensaje = fuente.render("Ingrese su nombre:", True, COLOR_TEXTO)
        pantalla.blit(
            mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - 100))

        # Mostrar el nombre ingresado hasta ahora
        texto_nombre = fuente.render(nombre, True, COLOR_TEXTO)
        pantalla.blit(
            texto_nombre, (ANCHO // 2 -
                           texto_nombre.get_width() // 2, ALTO // 2)
        )

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if (
                    evento.key == pygame.K_RETURN
                ):  # Presionar Enter para confirmar el nombre
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar el último carácter
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode  # Agregar caracteres al nombre

    return nombre


# Función que guarde la puntuación
def guardar_puntuacion(puntuacion, nombre="Jugador"):
    leaderboard = []
    archivo = "leaderboard.json"

    # Leer archivo de leaderboard si existe
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            leaderboard = json.load(f)

    # Añadir la nueva puntuación
    leaderboard.append({"nombre": nombre, "puntuacion": puntuacion})

    # Ordenar el leaderboard y mantener sólo los 5 mejores
    leaderboard = sorted(
        leaderboard, key=lambda x: x["puntuacion"], reverse=True)[:5]

    # Guardar de nuevo en el archivo
    with open(archivo, "w") as f:
        json.dump(leaderboard, f)

    return leaderboard


# Función para crear un nuevo obstáculo
def crear_obstaculo(MARGEN_CARRETERA, ANCHO, obstaculo_imagen, obstaculos):
    # Máximo número de intentos para colocar un obstáculo sin que esté superpuesto
    max_intentos = 10
    for _ in range(max_intentos):
        x_obstaculo = random.randint(
            MARGEN_CARRETERA, ANCHO - MARGEN_CARRETERA - obstaculo_imagen.get_width()
        )
        obstaculo_rect = obstaculo_imagen.get_rect(
            topleft=(x_obstaculo, -obstaculo_imagen.get_height())
        )

        # Verificar si el nuevo obstáculo está muy cerca de otros obstáculos
        superpuesto = False
        for obstaculo in obstaculos:
            if obstaculo_rect.colliderect(obstaculo["rect"]):
                superpuesto = True
                break

        if not superpuesto:
            obstaculos.append(
                {"imagen": obstaculo_imagen, "rect": obstaculo_rect})
            break  # Salir del bucle si se ha colocado un obstáculo sin superposición


def actualizar_nivel(
    distancia_recorrida,
    nivel,
    DISTANCIA_PARA_SUBIR_NIVEL,
    VELOCIDAD_AUTO_BASE,
    INCREMENTO_VELOCIDAD_AUTO,
    VELOCIDAD_AUTO_MAX,
    VELOCIDAD_CARRETERA_BASE,
    INCREMENTO_VELOCIDAD_CARRETERA,
    VELOCIDAD_CARRETERA_MAX,
    VELOCIDAD_OBSTACULO_BASE,
    INCREMENTO_VELOCIDAD_OBSTACULO,
    VELOCIDAD_OBSTACULO_MAX,
    velocidad_auto,
    velocidad_carretera,
    velocidad_obstaculo,
):
    if distancia_recorrida >= nivel * DISTANCIA_PARA_SUBIR_NIVEL:
        nivel += 1
        velocidad_auto = min(
            VELOCIDAD_AUTO_BASE + (nivel * INCREMENTO_VELOCIDAD_AUTO),
            VELOCIDAD_AUTO_MAX,
        )
        velocidad_carretera = min(
            VELOCIDAD_CARRETERA_BASE +
            (nivel * INCREMENTO_VELOCIDAD_CARRETERA),
            VELOCIDAD_CARRETERA_MAX,
        )
        velocidad_obstaculo = min(
            VELOCIDAD_OBSTACULO_BASE +
            (nivel * INCREMENTO_VELOCIDAD_OBSTACULO),
            VELOCIDAD_OBSTACULO_MAX,
        )
    return nivel, velocidad_auto, velocidad_carretera, velocidad_obstaculo


# Función para mostrar la pantalla de "Game Over" con botones
def mostrar_pantalla_game_over(
    pantalla, fuente, puntuacion, ANCHO, ALTO, COLOR_GAME_OVER, nombre
):
    pantalla.fill(COLOR_GAME_OVER)

    # Tamaño más grande para "Game Over"
    fuente_game_over = pygame.font.Font(None, 72)
    fuente_puntuacion = pygame.font.Font(None, 48)

    # Renderizar y dibujar el texto de "Game Over"
    texto_game_over = fuente_game_over.render(
        f"¡Game Over!", True, (255, 0, 0))
    pantalla.blit(
        texto_game_over,
        (
            ANCHO // 2 - texto_game_over.get_width() // 2,
            ALTO // 2 - texto_game_over.get_height() // 2 - 60,
        ),
    )

    # Guardar la puntuación y obtener el leaderboard
    leaderboard = guardar_puntuacion(puntuacion, nombre)

    # Mostrar el leaderboard
    y_offset = 50
    encabezado = fuente.render("Leaderboard:", True, (255, 255, 255))
    pantalla.blit(
        encabezado, (ANCHO - 200, y_offset)
    )  # Mover el encabezado a la derecha
    y_offset += 40

    for idx, entrada in enumerate(
        leaderboard[:10]
    ):  # Limitar a los primeros 10 puntajes
        texto = fuente.render(
            f"{idx + 1}. {entrada['nombre']}: {entrada['puntuacion']}",
            True,
            (255, 255, 255),
        )
        # Mover el texto a la derecha
        pantalla.blit(texto, (ANCHO - 200, y_offset))
        y_offset += 30

    # Renderizar y dibujar el texto de la puntuación con un gap de 20 píxeles
    texto_puntuacion = fuente.render(
        f"{nombre}: {puntuacion} puntos", True, COLOR_TEXTO
    )
    pantalla.blit(
        texto_puntuacion,
        (
            ANCHO // 2 - texto_puntuacion.get_width() // 2,
            ALTO // 2 - texto_puntuacion.get_height() // 2,
        ),
    )

    # Crear botones de pantalla de end game, moviéndolos más abajo
    boton_reiniciar = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 40, 200, 50)
    boton_salir = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50)

    pygame.draw.rect(pantalla, (0, 255, 0), boton_reiniciar)
    pygame.draw.rect(pantalla, (255, 0, 0), boton_salir)

    texto_reiniciar = fuente.render("Reiniciar (R)", True, (0, 0, 0))
    texto_salir = fuente.render("Salir (Q)", True, (0, 0, 0))

    pantalla.blit(
        texto_reiniciar,
        (
            boton_reiniciar.x
            + (boton_reiniciar.width - texto_reiniciar.get_width()) // 2,
            boton_reiniciar.y
            + (boton_reiniciar.height - texto_reiniciar.get_height()) // 2,
        ),
    )
    pantalla.blit(
        texto_salir,
        (
            boton_salir.x + (boton_salir.width - texto_salir.get_width()) // 2,
            boton_salir.y + (boton_salir.height -
                             texto_salir.get_height()) // 2,
        ),
    )

    pygame.display.flip()

    # Esperar a que el jugador haga clic en un botón o presione una tecla
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(evento.pos):
                    return True  # Reiniciar el juego
                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True  # Reiniciar el juego
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def mostrar_pantalla_pausa(pantalla, fuente_pausa, ANCHO, ALTO):
    # Crear una superficie semitransparente para nublar la pantalla
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(128)  # Ajustar la transparencia (0-255)
    overlay.fill((0, 0, 0))  # Color negro

    # Dibujar la superficie semitransparente sobre la pantalla
    pantalla.blit(overlay, (0, 0))

    # Crear el texto de pausa
    texto_pausa = fuente_pausa.render("PAUSA", True, (255, 255, 255))

    # Calcular la posición del texto de pausa
    rect_pausa = texto_pausa.get_rect(center=(ANCHO // 2, ALTO // 2))

    # Dibujar el texto de pausa sobre la pantalla nublada
    pantalla.blit(texto_pausa, rect_pausa)

def renderizar_fondo(estado_fondo, pantalla):
    if estado_fondo == 0:  # Día
        pantalla.fill((135, 206, 235))  # Fondo color celeste cielo para el día
    elif estado_fondo == 1:  # Noche
        pantalla.fill((0, 0, 0))  # Fondo negro para la noche
    elif estado_fondo == 2:  # Lluvia
        pantalla.fill((100, 100, 100))  # Fondo gris para lluvia
    elif estado_fondo == 3:  # Nieve
        pantalla.fill((200, 200, 200))  # Fondo gris claro para nieve
