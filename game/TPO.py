import pygame
import sys
import os
import random
# tkinter libreria de python para usar js en el front
from PIL import Image, ImageEnhance  # Importar Pillow
from utils.constants import *
from utils.functions import *

# Inicializar Pygame
pygame.init()

# Cambiar el directorio de trabajo al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ruta relativa de la imagen
ruta_auto = 'assets/img/autoamarillo.png'
ruta_obstaculo = 'assets/img/auto.png'
ruta_cactus = 'assets/img/cactus.png'

# Imprimir la ruta absoluta para verificar
print("Ruta absoluta del auto:", os.path.abspath(ruta_auto))
print("Ruta absoluta del obstáculo:", os.path.abspath(ruta_obstaculo))
print("Ruta absoluta del cactus:", os.path.abspath(ruta_cactus))


# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Autos")

# Cargar la imagen del auto con transparencia
try:
    auto_imagen = pygame.image.load(ruta_auto).convert_alpha()
    auto_imagen = pygame.transform.scale(auto_imagen, (72, 130))
except pygame.error:
    print("No se pudo cargar la imagen del auto. Asegúrate de tener un archivo '.png' en el directorio.")
    pygame.quit()
    sys.exit()

auto_rect = auto_imagen.get_rect(center=(ANCHO // 2, ALTO - 60))

# Cargar la imagen del auto obstáculo
try:
    obstaculo_imagen = pygame.image.load(ruta_obstaculo).convert_alpha()
    obstaculo_imagen = pygame.transform.scale(obstaculo_imagen, (45, 65))
except pygame.error:
    print("No se pudo cargar la imagen del obstáculo.")
    pygame.quit()
    sys.exit()


# Cargar la imagen del cactus y ajustar el brillo
try:
    cactus_imagen_pil = Image.open(ruta_cactus).convert("RGBA")
    enhancer = ImageEnhance.Brightness(cactus_imagen_pil)
    cactus_imagen_pil = enhancer.enhance(1.7)  
    cactus_imagen = pygame.image.fromstring(cactus_imagen_pil.tobytes(), cactus_imagen_pil.size, cactus_imagen_pil.mode)
    cactus_imagen = pygame.transform.scale(cactus_imagen, (50, 68))  
except pygame.error:
    print("No se pudo cargar la imagen del cactus. Asegúrate de tener un archivo 'cactus.png' en el directorio 'assets/img'.")
    pygame.quit()
    sys.exit()


# Crear la carretera
carretera_superior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_superior.fill(COLOR_CARRETERA)
carretera_rect_superior = carretera_superior.get_rect(topleft=(MARGEN_CARRETERA, 0))

carretera_inferior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_inferior.fill(COLOR_CARRETERA)
carretera_rect_inferior = carretera_inferior.get_rect(topleft=(MARGEN_CARRETERA, -ALTO))

# Fuente para mostrar la distancia y la puntuación
fuente = pygame.font.Font(None, 36)
# Fuente más grande para el texto de pausa
fuente_pausa = pygame.font.Font(None, 72)

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Función para reiniciar el juego
def reiniciar_juego(VELOCIDAD_AUTO_BASE, VELOCIDAD_CARRETERA_BASE, VELOCIDAD_OBSTACULO_BASE, auto_imagen, ANCHO, ALTO):
    global distancia_recorrida, puntuacion, velocidad_auto, velocidad_carretera, velocidad_obstaculo, nivel, obstaculos, auto_rect
    distancia_recorrida = 0
    puntuacion = 0
    velocidad_auto = VELOCIDAD_AUTO_BASE
    velocidad_carretera = VELOCIDAD_CARRETERA_BASE
    velocidad_obstaculo = VELOCIDAD_OBSTACULO_BASE
    nivel = 1
    obstaculos = []
    auto_rect = auto_imagen.get_rect(center=(ANCHO // 2, ALTO - 60))

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pausado = not pausado  # Alternar el estado de pausa

    if not pausado:
        # Lógica del juego cuando no está en pausa
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            auto_rect.y -= VELOCIDAD_AUTO_BASE
        if teclas[pygame.K_DOWN]:
            auto_rect.y += VELOCIDAD_AUTO_BASE
        if teclas[pygame.K_LEFT]:
            auto_rect.x -= VELOCIDAD_AUTO_BASE
        if teclas[pygame.K_RIGHT]:
            auto_rect.x += VELOCIDAD_AUTO_BASE

        # Mantener el auto dentro de la carretera
        if auto_rect.left < MARGEN_CARRETERA:
            auto_rect.left = MARGEN_CARRETERA
        if auto_rect.right > ANCHO - MARGEN_CARRETERA:
            auto_rect.right = ANCHO - MARGEN_CARRETERA

        # Mantener el auto dentro de la pantalla
        auto_rect.y = max(0, min(auto_rect.y, ALTO - auto_rect.height))

        # Mover la carretera
        carretera_rect_superior.y += VELOCIDAD_CARRETERA_BASE
        carretera_rect_inferior.y += VELOCIDAD_CARRETERA_BASE

        # Actualizar la distancia recorrida
        distancia_recorrida += VELOCIDAD_CARRETERA_BASE / FPS

        # Actualizar el nivel y las velocidades
        nivel, velocidad_auto, velocidad_carretera, velocidad_obstaculo = actualizar_nivel(
            distancia_recorrida, nivel, DISTANCIA_PARA_SUBIR_NIVEL, VELOCIDAD_AUTO_BASE, INCREMENTO_VELOCIDAD_AUTO, VELOCIDAD_AUTO_MAX,
            VELOCIDAD_CARRETERA_BASE, INCREMENTO_VELOCIDAD_CARRETERA, VELOCIDAD_CARRETERA_MAX,
            VELOCIDAD_OBSTACULO_BASE, INCREMENTO_VELOCIDAD_OBSTACULO, VELOCIDAD_OBSTACULO_MAX,
            velocidad_auto, velocidad_carretera, velocidad_obstaculo
        )

        # Volver a posicionar la carretera
        if carretera_rect_superior.y >= ALTO:
            carretera_rect_superior.y = carretera_rect_inferior.y - ALTO
        if carretera_rect_inferior.y >= ALTO:
            carretera_rect_inferior.y = carretera_rect_superior.y - ALTO

        # Crear un nuevo obstáculo de forma aleatoria
        if random.randint(0, 100) < 1:  # 1% de probabilidad por frame de crear un nuevo obstáculo
            crear_obstaculo(MARGEN_CARRETERA, ANCHO, obstaculo_imagen, obstaculos)
        if random.randint(0, 100) < 1:  # 1% de probabilidad por frame de crear un nuevo obstáculo
            crear_obstaculo(MARGEN_CARRETERA, ANCHO, cactus_imagen, obstaculos)
            
        # Mover los obstáculos y detectar colisiones
        for obstaculo in obstaculos:
            obstaculo['rect'].y += VELOCIDAD_OBSTACULO_BASE
            if auto_rect.colliderect(obstaculo['rect']):
                print("¡Choque! Juego terminado.")
                if mostrar_pantalla_game_over(pantalla, fuente, puntuacion, ANCHO, ALTO, COLOR_GAME_OVER):
                    reiniciar_juego(VELOCIDAD_AUTO_BASE, VELOCIDAD_CARRETERA_BASE, VELOCIDAD_OBSTACULO_BASE, auto_imagen, ANCHO, ALTO)
                else:
                    pygame.quit()
                    sys.exit()

        # Eliminar obstáculos que han salido de la pantalla y aumentar la puntuación
        nuevos_obstaculos = []
        for obstaculo in obstaculos:
            if obstaculo['rect'].y >= ALTO:
                puntuacion += 1
            else:
                nuevos_obstaculos.append(obstaculo)
        obstaculos = nuevos_obstaculos

    # Actualizar la pantalla
    pantalla.fill(COLOR_FONDO)

    # Dibujar carretera
    pantalla.blit(carretera_superior, carretera_rect_superior)
    pantalla.blit(carretera_inferior, carretera_rect_inferior)

    # Dibujar líneas en la carretera (rectas y verticales)
    linea_ancho = 8
    linea_largo = 16
    distancia_entre_lineas = 40
    for y in range(carretera_rect_superior.y % (linea_largo + distancia_entre_lineas), ALTO, linea_largo + distancia_entre_lineas):
        pygame.draw.line(pantalla, COLOR_LINEA, 
                         (ANCHO // 2, y), 
                         (ANCHO // 2, y + linea_largo), 
                            linea_ancho)

    # Dibujar el auto
    pantalla.blit(auto_imagen, auto_rect)

    # Dibujar obstáculos
    for obstaculo in obstaculos:
        pantalla.blit(obstaculo['imagen'], obstaculo['rect'])

    # Mostrar la distancia y la puntuación
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255, 255, 255))
    texto_distancia = fuente.render(f"Distancia: ", True, (255, 255, 255))
    texto_puntuacion_valor = fuente.render(f"{int(distancia_recorrida)} mts", True, (255, 255, 255))
    pantalla.blit(texto_puntuacion, (10, 10))
    pantalla.blit(texto_nivel, (10, 60))
    pantalla.blit(texto_distancia, (10, 100))
    pantalla.blit(texto_puntuacion_valor, (10, 130))  # Ajustar la coordenada y para que esté en el siguiente renglón

    
    if pausado:
        mostrar_pantalla_pausa(pantalla, fuente_pausa, ANCHO, ALTO)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(FPS)