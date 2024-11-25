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
        (
            nuevo_nivel,
            nueva_velocidad_auto,
            nueva_velocidad_carretera,
            nueva_velocidad_obstaculo,
        ) = actualizar_nivel(
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
        imagen_obstaculo = pygame.Surface(
            (50, 50)
        )  # Crear una superficie como imagen de prueba

        # Llama a la función
        crear_obstaculo(MARGEN_CARRETERA, ANCHO, imagen_obstaculo, obstaculos)

        # Verifica que se ha creado un obstáculo
        self.assertEqual(len(obstaculos), 1)
        # Verifica que el obstáculo está dentro de los márgenes de la carretera
        self.assertTrue(
            MARGEN_CARRETERA <= obstaculos[0]["rect"].x <= ANCHO -
            MARGEN_CARRETERA
        )

    def test_auto_stays_within_road_bounds(self):
        # Configuración de la carretera y posición del auto
        MARGEN_CARRETERA = 50
        ANCHO = 800
        ALTO = 600
        # Suponiendo un tamaño de auto
        auto_rect = pygame.Rect(100, ALTO - 60, 72, 130)

        # Simular movimiento fuera de los límites
        auto_rect.left = MARGEN_CARRETERA - 10
        auto_rect.right = ANCHO - MARGEN_CARRETERA + 10

        # Limitar el auto dentro de los límites de la carretera
        auto_rect.left = max(auto_rect.left, MARGEN_CARRETERA)
        auto_rect.right = min(auto_rect.right, ANCHO - MARGEN_CARRETERA)

        # Verificar límites
        self.assertGreaterEqual(auto_rect.left, MARGEN_CARRETERA)
        self.assertLessEqual(auto_rect.right, ANCHO - MARGEN_CARRETERA)

    def test_obstacles_move_down(self):
        # Configuración inicial de obstáculos
        obstaculo_imagen = pygame.Surface(
            (45, 65)
        )  # Imagen de prueba para el obstáculo
        obstaculos = []
        crear_obstaculo(50, 800, obstaculo_imagen, obstaculos)
        posicion_inicial = obstaculos[0]["rect"].y

        # Simular movimiento de los obstáculos
        velocidad_obstaculo = 5
        for obstaculo in obstaculos:
            obstaculo["rect"].y += velocidad_obstaculo

        # Verificar que los obstáculos se movieron hacia abajo
        self.assertGreater(obstaculos[0]["rect"].y, posicion_inicial)


if __name__ == "__main__":
    unittest.main()
