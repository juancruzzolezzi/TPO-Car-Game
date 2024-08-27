import pygame
import sys

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
VELOCIDAD_CARRETERA = 5
ANCHO_CARRETERA = 400
MARGEN_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2  # Centrando la carretera

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Autos con Carretera Infinita")

# Cargar la imagen del auto con transparencia
try:
    auto_imagen = pygame.image.load('auto.png').convert_alpha()
    auto_imagen = pygame.transform.scale(auto_imagen, (75, 125))  # Ajustar el tamaño si es necesario
except pygame.error:
    print("No se pudo cargar la imagen del auto. Asegúrate de tener un archivo 'auto.png' en el directorio.")
    pygame.quit()
    sys.exit()

auto_rect = auto_imagen.get_rect(center=(ANCHO // 2, ALTO - 60))

# Crear la carretera
carretera_superior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_superior.fill(COLOR_CARRETERA)
carretera_rect_superior = carretera_superior.get_rect(topleft=(MARGEN_CARRETERA, 0))

carretera_inferior = pygame.Surface((ANCHO_CARRETERA, ALTO))
carretera_inferior.fill(COLOR_CARRETERA)
carretera_rect_inferior = carretera_inferior.get_rect(topleft=(MARGEN_CARRETERA, -ALTO))

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

    # Actualizar la pantalla
    pantalla.fill(COLOR_FONDO)

    # Dibujar carretera
    pantalla.blit(carretera_superior, carretera_rect_superior)
    pantalla.blit(carretera_inferior, carretera_rect_inferior)
    
    # Dibujar líneas en la carretera (rectas y verticales)
    linea_ancho = 8  # Ajusta el ancho de las líneas aquí
    linea_largo = 16  # Ajusta el largo de las líneas aquí
    distancia_entre_lineas = 40  # Ajusta la distancia entre las líneas aquí
    for y in range(carretera_rect_superior.y % (linea_largo + distancia_entre_lineas), ALTO, linea_largo + distancia_entre_lineas):
        pygame.draw.line(pantalla, COLOR_LINEA, 
                         (ANCHO // 2, y), 
                         (ANCHO // 2, y + linea_largo), 
                         linea_ancho)
    
    # Dibujar el auto
    pantalla.blit(auto_imagen, auto_rect)
    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(FPS)