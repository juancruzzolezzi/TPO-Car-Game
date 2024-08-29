import pygame
import sys
import os
import random

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
COLOR_FONDO = (16, 174, 6)  # Verde pasto (Lawn Green)
COLOR_CARRETERA = (50, 50, 50)  # Gris oscuro
COLOR_LINEA = (255, 255, 255)  # Blanco para las líneas de la carretera
FPS = 60
VELOCIDAD_AUTO = 5
VELOCIDAD_CARRETERA = 4
VELOCIDAD_OBSTACULO = 7
INCREMENTO_VELOCIDAD = 0.5
ANCHO_CARRETERA = 400
MARGEN_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2  # Centrando la carretera

# Cambiar el directorio de trabajo al directorio del script (con esto se puede modularizar el codigo)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ruta relativa de la imagen
ruta_auto = '../img/f1real.png'
ruta_obstaculo = '../img/auto.png'

# Imprimir la ruta absoluta para verificar
print("Ruta absoluta del auto:", os.path.abspath(ruta_auto))
print("Ruta absoluta del obstáculo:", os.path.abspath(ruta_obstaculo))

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Autos con Carretera Infinita")

# Cargar la imagen del auto con transparencia
try:
    auto_imagen = pygame.image.load(ruta_auto).convert_alpha()
    auto_imagen = pygame.transform.scale(auto_imagen, (72, 130))  # Ajustar el tamaño si es necesario
except pygame.error:
    print("No se pudo cargar la imagen del auto. Asegúrate de tener un archivo '.png' en el directorio.")
    pygame.quit()
    sys.exit()

auto_rect = auto_imagen.get_rect(center=(ANCHO // 2, ALTO - 60))

# Cargar la imagen del obstáculo
try:
    obstaculo_imagen = pygame.image.load(ruta_obstaculo).convert_alpha()
    obstaculo_imagen = pygame.transform.scale(obstaculo_imagen, (50, 50))  # Ajustar el tamaño si es necesario
except pygame.error:
    print("No se pudo cargar la imagen del obstáculo. Asegúrate de tener un archivo '.png' en el directorio.")
    pygame.quit()
    sys.exit()

# Lista para almacenar los obstáculos
obstaculos = []

# Crear la carretera
carretera_superior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_superior.fill(COLOR_CARRETERA)
carretera_rect_superior = carretera_superior.get_rect(topleft=(MARGEN_CARRETERA, 0))

carretera_inferior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_inferior.fill(COLOR_CARRETERA)
carretera_rect_inferior = carretera_inferior.get_rect(topleft=(MARGEN_CARRETERA, -ALTO))

# Función para crear un nuevo obstáculo
def crear_obstaculo():
    x_obstaculo = random.randint(MARGEN_CARRETERA, ANCHO - MARGEN_CARRETERA - obstaculo_imagen.get_width())
    obstaculo_rect = obstaculo_imagen.get_rect(topleft=(x_obstaculo, -obstaculo_imagen.get_height()))
    obstaculos.append(obstaculo_rect)

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if (evento.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

    # Manejar entrada del teclado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]:
        auto_rect.y -= VELOCIDAD_AUTO
    if teclas[pygame.K_DOWN]:
        auto_rect.y += VELOCIDAD_AUTO
    if teclas[pygame.K_LEFT]:
        auto_rect.x -= VELOCIDAD_AUTO
    if teclas[pygame.K_RIGHT]:
        auto_rect.x += VELOCIDAD_AUTO

    # Mantener el auto dentro de la carretera
    if auto_rect.left < MARGEN_CARRETERA:
        auto_rect.left = MARGEN_CARRETERA
    if auto_rect.right > ANCHO - MARGEN_CARRETERA:
        auto_rect.right = ANCHO - MARGEN_CARRETERA

    # Mantener el auto dentro de la pantalla
    auto_rect.y = max(0, min(auto_rect.y, ALTO - auto_rect.height))

    # Mover la carretera
    carretera_rect_superior.y += VELOCIDAD_CARRETERA
    carretera_rect_inferior.y += VELOCIDAD_CARRETERA

    # Volver a posicionar la carretera
    if carretera_rect_superior.y >= ALTO:
        carretera_rect_superior.y = carretera_rect_inferior.y - ALTO
    if carretera_rect_inferior.y >= ALTO:
        carretera_rect_inferior.y = carretera_rect_superior.y - ALTO

    # Crear un nuevo obstáculo de forma aleatoria
    if random.randint(0, 100) < 1:  # 1% de probabilidad por frame de crear un nuevo obstáculo
        crear_obstaculo()

    # Mover los obstáculos y detectar colisiones
    for obstaculo in obstaculos:
        obstaculo.y += VELOCIDAD_OBSTACULO
        if auto_rect.colliderect(obstaculo):
            print("¡Choque! Juego terminado.")
            pygame.quit()
            sys.exit()

    # Eliminar los obstáculos que salen de la pantalla
    obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo.y < ALTO]

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
        pantalla.blit(obstaculo_imagen, obstaculo)

    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(FPS)
