import unittest
from utils.functions import actualizar_nivel, crear_obstaculo
import pygame

# Inicia Pygame para poder trabajar con Surfaces en las pruebas
pygame.init()

class TestFunctions(unittest.TestCase):
    def test_actualizar_nivel(self):
        # Valores de prueba
        distancia_recorrida = 1000
        nivel = 1
        DISTANCIA_PARA_SUBIR_NIVEL = 1000
        VELOCIDAD_AUTO_BASE = 5
        INCREMENTO_VELOCIDAD_AUTO = 1
        VELOCIDAD_AUTO_MAX = 10
        VELOCIDAD_CARRETERA_BASE = 2
        INCREMENTO_VELOCIDAD_CARRETERA = 0.5
        VELOCIDAD_CARRETERA_MAX = 5
        VELOCIDAD_OBSTACULO_BASE = 3
        INCREMENTO_VELOCIDAD_OBSTACULO = 0.3
        VELOCIDAD_OBSTACULO_MAX = 6
        velocidad_auto = VELOCIDAD_AUTO_BASE
        velocidad_carretera = VELOCIDAD_CARRETERA_BASE
        velocidad_obstaculo = VELOCIDAD_OBSTACULO_BASE

        # Llama a la función
        nuevo_nivel, nueva_velocidad_auto, nueva_velocidad_carretera, nueva_velocidad_obstaculo = actualizar_nivel(
            distancia_recorrida, nivel, DISTANCIA_PARA_SUBIR_NIVEL,
            VELOCIDAD_AUTO_BASE, INCREMENTO_VELOCIDAD_AUTO, VELOCIDAD_AUTO_MAX,
            VELOCIDAD_CARRETERA_BASE, INCREMENTO_VELOCIDAD_CARRETERA, VELOCIDAD_CARRETERA_MAX,
            VELOCIDAD_OBSTACULO_BASE, INCREMENTO_VELOCIDAD_OBSTACULO, VELOCIDAD_OBSTACULO_MAX,
            velocidad_auto, velocidad_carretera, velocidad_obstaculo
        )

        # Pruebas de verificación
        self.assertEqual(nuevo_nivel, nivel + 1)
        self.assertTrue(nueva_velocidad_auto <= VELOCIDAD_AUTO_MAX)
        self.assertTrue(nueva_velocidad_carretera <= VELOCIDAD_CARRETERA_MAX)
        self.assertTrue(nueva_velocidad_obstaculo <= VELOCIDAD_OBSTACULO_MAX)

    def test_crear_obstaculo(self):
        MARGEN_CARRETERA = 100
        ANCHO = 800
        obstaculos = []
        imagen_obstaculo = pygame.Surface((50, 50))  # Crear una superficie como imagen de prueba

        # Llama a la función
        crear_obstaculo(MARGEN_CARRETERA, ANCHO, imagen_obstaculo, obstaculos)

        # Verifica que se ha creado un obstáculo
        self.assertEqual(len(obstaculos), 1)
        # Verifica que el obstáculo está dentro de los márgenes de la carretera
        self.assertTrue(MARGEN_CARRETERA <= obstaculos[0]['rect'].x <= ANCHO - MARGEN_CARRETERA)

if __name__ == '__main__':
    unittest.main()
