# Constantes
ANCHO = 800
ALTO = 600
COLOR_FONDO = (16, 174, 6)  # Verde pasto (Lawn Green)
COLOR_GAME_OVER = (0, 0, 0)
COLOR_CARRETERA = (50, 50, 50)  # Gris oscuro
COLOR_LINEA = (255, 255, 255)  # Blanco para las líneas de la carretera
FPS = 60
INCREMENTO_VELOCIDAD_AUTO = 1
INCREMENTO_VELOCIDAD_CARRETERA = 5
INCREMENTO_VELOCIDAD_OBSTACULO = 2
ANCHO_CARRETERA = 400
MARGEN_CARRETERA = (ANCHO - ANCHO_CARRETERA) // 2  # Centrando la carretera

# Inicializar variables de distancia y puntuación
distancia_recorrida = 0
puntuacion = 0

# Constantes modificadas
VELOCIDAD_AUTO_BASE = 8
VELOCIDAD_CARRETERA_BASE = 12
VELOCIDAD_OBSTACULO_BASE = 9

VELOCIDAD_AUTO_MAX = 32
VELOCIDAD_CARRETERA_MAX = 50
VELOCIDAD_OBSTACULO_MAX = 30

DISTANCIA_PARA_SUBIR_NIVEL = 100

# Inicializar variables de velocidad y nivel del juego
velocidad_auto = VELOCIDAD_AUTO_BASE
velocidad_carretera = VELOCIDAD_CARRETERA_BASE
velocidad_obstaculo = VELOCIDAD_OBSTACULO_BASE

nivel = 1

# Lista para almacenar los obstáculos
obstaculos = []