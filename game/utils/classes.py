# Clases
import pygame
import random
from .constants import *

ANCHO, ALTO = 800, 600


class Nieve:
    def __init__(self, cantidad, pantalla):
        self.particulas = []
        self.pantalla = pantalla
        for _ in range(cantidad):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            self.particulas.append([x, y])

    def actualizar(self):
        for particula in self.particulas:
            particula[1] += 1
            if particula[1] > ALTO:
                particula[1] = random.randint(-20, -1)
                particula[0] = random.randint(0, ANCHO)

    def dibujar(self):
        for particula in self.particulas:
            pygame.draw.circle(self.pantalla, (255, 255, 255), particula, 2)


class Lluvia:
    def __init__(self, cantidad, pantalla):
        self.particulas = []
        self.pantalla = pantalla
        for _ in range(cantidad):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            self.particulas.append([x, y])

    def actualizar(self):
        for particula in self.particulas:
            particula[1] += 5
            if particula[1] > ALTO:
                particula[1] = random.randint(-20, -1)
                particula[0] = random.randint(0, ANCHO)

    def dibujar(self):
        for particula in self.particulas:
            pygame.draw.line(
                self.pantalla,
                (0, 0, 255),
                particula,
                (particula[0], particula[1] + 5),
                1,
            )
