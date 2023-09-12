import pygame
import math

class Bala:
    def __init__(self, x, y, target_x, target_y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad

        dx = target_x - x
        dy = target_y - y
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        if distancia == 0:
            distancia = 1 
        self.dx = dx / distancia * velocidad
        self.dy = dy / distancia * velocidad

    def mover(self):
        self.x += self.dx
        self.y += self.dy

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, (255, 0, 0), (int(self.x), int(self.y)), 5)