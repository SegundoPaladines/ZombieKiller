import pygame
import random

class Zombie:
    def __init__(self, screen_width, screen_height, dificultad, target):
        self.x = random.randint(0, screen_width)  # Valor aleatorio entre 0 y el ancho de la pantalla
        self.y = random.choice([0, screen_height])  # Genera en la parte superior o inferior de la pantalla
        self.velocidad = 1
        self.damage = 0
        self.image = "img/zombie.png"
        self.target = target

        if dificultad == "Fácil":
            self.velocidad += 1
            self.damage += 5
        elif dificultad == "Medio":
            self.velocidad += 2
            self.damage += 10
        elif dificultad == "Difícil":
            self.velocidad += 3
            self.damage += 25
        elif dificultad == "Infierno":
            self.velocidad = 5
            self.damage += 25

    def mover(self):
        # Calcula la dirección hacia la que debe moverse el zombie para perseguir al objetivo (target)
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distancia = max(1, abs(dx) + abs(dy))  # Evita la división por cero
        direccion_x = dx / distancia
        direccion_y = dy / distancia

        # Actualiza la posición del zombie en función de la dirección calculada
        self.x += direccion_x * self.velocidad
        self.y += direccion_y * self.velocidad

    def dibujar(self, ventana):
        # Carga la imagen del zombie y la dibuja en la posición actual
        zombie_img = pygame.image.load(self.image)
        zombie_img = pygame.transform.scale(zombie_img, (50, 50))
        ventana.blit(zombie_img, (self.x, self.y))