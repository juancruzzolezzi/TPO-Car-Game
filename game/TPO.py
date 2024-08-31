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
# VELOCIDAD_AUTO = 25
# VELOCIDAD_CARRETERA = 50
# VELOCIDAD_OBSTACULO = 22
INCREMENTO_VELOCIDAD_AUTO = 1
INCREMENTO_VELOCIDAD_CARRETERA = 5
INCREMENTO_VELOCIDAD_OBSTACULO = 2
ANCHO_CARRETERA = 400
MARGEN_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2  # Centrando la carretera

# Inicializar variables de distancia y puntuación
distancia_recorrida = 0
puntuacion = 0

# Constantes modificadas
VELOCIDAD_AUTO_BASE = 7
VELOCIDAD_CARRETERA_BASE = 12
VELOCIDAD_OBSTACULO_BASE = 9

VELOCIDAD_AUTO_MAX = 32
VELOCIDAD_CARRETERA_MAX = 50
VELOCIDAD_OBSTACULO_MAX = 30

DISTANCIA_PARA_SUBIR_NIVEL = 100

# Inicializar variables de velocidad
velocidad_auto = VELOCIDAD_AUTO_BASE
velocidad_carretera = VELOCIDAD_CARRETERA_BASE
velocidad_obstaculo = VELOCIDAD_OBSTACULO_BASE

nivel = 1

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
pygame.display.set_caption("Juego de Autos")

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

# Fuente para mostrar la distancia y la puntuación
fuente = pygame.font.Font(None, 36)

# Función para crear un nuevo obstáculo
def crear_obstaculo():
    max_intentos = 10  # Máximo número de intentos para colocar un obstáculo sin que esté superpuesto
    for _ in range(max_intentos):
        x_obstaculo = random.randint(MARGEN_CARRETERA, ANCHO - MARGEN_CARRETERA - obstaculo_imagen.get_width())
        obstaculo_rect = obstaculo_imagen.get_rect(topleft=(x_obstaculo, -obstaculo_imagen.get_height()))

        # Verificar si el nuevo obstáculo está muy cerca de otros obstáculos
        superpuesto = False
        for obstaculo in obstaculos:
            if obstaculo_rect.colliderect(obstaculo):
                superpuesto = True
                break

        if not superpuesto:
            obstaculos.append(obstaculo_rect)
            break  # Salir del bucle si se ha colocado un obstáculo sin superposición

# Reloj para controlar FPS
reloj = pygame.time.Clock()

# Función para actualizar las velocidades y el nivel
def actualizar_nivel():
    global nivel, velocidad_auto, velocidad_carretera, velocidad_obstaculo

    if distancia_recorrida >= nivel * DISTANCIA_PARA_SUBIR_NIVEL:
        nivel += 1
        velocidad_auto = min(VELOCIDAD_AUTO_BASE + (nivel * INCREMENTO_VELOCIDAD_AUTO), VELOCIDAD_AUTO_MAX)
        velocidad_carretera = min(VELOCIDAD_CARRETERA_BASE + (nivel * INCREMENTO_VELOCIDAD_CARRETERA), VELOCIDAD_CARRETERA_MAX)
        velocidad_obstaculo = min(VELOCIDAD_OBSTACULO_BASE + (nivel * INCREMENTO_VELOCIDAD_OBSTACULO), VELOCIDAD_OBSTACULO_MAX)
        print(f"Nivel: {nivel} - Velocidad Auto: {velocidad_auto}, Velocidad Carretera: {velocidad_carretera}, Velocidad Obstáculo: {velocidad_obstaculo}")


# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if (evento.type == pygame.QUIT):
            pygame.quit()
            sys.exit()

    # Manejar entrada del teclado
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
    
    # Actualizar el nivel del juego
    actualizar_nivel()

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
        obstaculo.y += VELOCIDAD_OBSTACULO_BASE
        if auto_rect.colliderect(obstaculo):
            print("¡Choque! Juego terminado.")
            pygame.quit()
            sys.exit()

    # Eliminar obstáculos que han salido de la pantalla y aumentar la puntuación
    nuevos_obstaculos = []
    for obstaculo in obstaculos:
        if obstaculo.y >= ALTO:
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
        pantalla.blit(obstaculo_imagen, obstaculo)
        
    # Mostrar la distancia y la puntuación
    texto_distancia = fuente.render(f"Distancia: {int(distancia_recorrida)} mts", True, (255, 255, 255))
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255, 255, 255))
    pantalla.blit(texto_distancia, (10, 10))
    pantalla.blit(texto_puntuacion, (10, 40))
    pantalla.blit(texto_nivel, (10, 70))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(FPS)
