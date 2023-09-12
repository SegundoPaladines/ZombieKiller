import pygame
from shooter import Shooter
from zombie import Zombie
import time
from bala import Bala
import math

class Juego:
    def __init__(self, shooter):
        self.shooter = shooter
        self.estado = True

        #Tamaño de la ventana
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 600

        self.miraX = 550
        self.miraY = 200;

        self.mira_img = pygame.image.load("img/crosshair.png")
        self.mira_img = pygame.transform.scale(self.mira_img, (50, 50))

        self.shooter_img_original = pygame.image.load(self.shooter.img)
        self.shooter_img_original = pygame.transform.scale(self.shooter_img_original, (50, 50))
        self.shooter_img = self.shooter_img_original

        self.recarga_duracion = self.shooter.tiempoRecarga()
        self.recarga_tiempo = 0

        self.duracion_disparo = 0.05
        self.tiempo_disparo = 0

        self.duracion_generacion_z = 0.5
        self.tiempo_ultimo_z = 0

        self.balas = []
        self.zombies = []

    # Información en la ventana
    def mostrar_info(self, ventana):
        font = pygame.font.Font(None, 36)
        vida_text = font.render(f"Vida: {self.shooter.vida}", True, (255, 255, 255))
        municion_text = font.render(f"Municion: {self.shooter.municion}", True, (255, 255, 255))
        puntaje_text = font.render(f"Puntaje: {self.shooter.score}", True, (255, 255, 255))

        ventana.blit(vida_text, (10, 10))  # Posición de la barra de vida
        ventana.blit(municion_text, (10, 50))  # Posición de la munición
        ventana.blit(puntaje_text, (10, 90))  # Posición del puntaje

    def moverShooter(self, ventana):
        # Manejo de eventos de teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.shooter.moverIzquierda()
            if self.shooter.x < 0:
                self.shooter.x = 0  # Limita el movimiento hacia la izquierda
        if keys[pygame.K_RIGHT]:
            self.shooter.moverDerecha()
            if self.shooter.x + 50 > self.SCREEN_WIDTH:
                self.shooter.x = self.SCREEN_WIDTH - 50  # Limita el movimiento hacia la derecha

        # Dibuja al shooter en su posición actual
        shooter_x = self.shooter.x
        shooter_y = self.shooter.y
        shooter_img = pygame.image.load(self.shooter.img)
        shooter_img = pygame.transform.scale(shooter_img, (50, 50))

        # Dibuja el nombre del personaje arriba de él
        font = pygame.font.Font(None, 36)
        nombre_text = font.render(self.shooter.nombre, True, (255, 255, 255))
        nombre_rect = nombre_text.get_rect(center=(shooter_x + 25, shooter_y - 20))

        ventana.blit(nombre_text, nombre_rect)

    def disparar(self, ventana): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.tiempo_disparo == 0:
                self.tiempo_disparo = time.time()

            tiempo_actual = time.time()
            tiempo_transcurrido = tiempo_actual - self.tiempo_disparo
            
            if self.shooter.municion > 0 and tiempo_transcurrido >= self.duracion_disparo:
                # Crear una nueva bala desde la posición del jugador hacia la mira
                nueva_bala = Bala(self.shooter.x+25, self.shooter.y+20, self.miraX, self.miraY, velocidad=100)
                self.balas.append(nueva_bala)
                self.shooter.disparar()
                self.actualizar_info(ventana)
                self.tiempo_disparo = 0

    def recargar(self, ventana):
        if self.shooter.municion <= 0:
            if self.recarga_tiempo == 0:
                self.recarga_tiempo = time.time()

            tiempo_actual = time.time()
            tiempo_transcurrido = tiempo_actual - self.recarga_tiempo

            # Comprobar si ya se ha pasado suficiente tiempo para recargar
            if tiempo_transcurrido >= self.recarga_duracion:
                self.recarga_tiempo = 0
                self.shooter.recargar()
                self.actualizar_info(ventana)
            else:
                self.mostrar_recargando(ventana)

    def mostrar_recargando(self, ventana):
        font = pygame.font.Font(None, 36)
        recargando_text = font.render("Recargando...", True, (255, 0, 0))
        text_rect = recargando_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        ventana.blit(recargando_text, text_rect)
    
    def actualizar_balas(self):
        for bala in self.balas:
            bala.mover()
            # Eliminar la bala cuando alcance el borde derecho de la pantalla
            if bala.x > self.SCREEN_WIDTH:
                self.balas.remove(bala)
            else:
                # Verificar colisiones con zombies
                for zombie in self.zombies:
                    if bala.x < zombie.x + 50 and bala.x + 10 > zombie.x and \
                    bala.y < zombie.y + 50 and bala.y + 10 > zombie.y:
                        # Si la bala colisiona con un zombie, elimina la bala y el zombie
                        self.balas.remove(bala)
                        self.zombies.remove(zombie)

                        self.shooter.score += 1 
                        break

    def dibujar_balas(self, ventana):
        for bala in self.balas:
            bala.dibujar(ventana)

    def actualizar_info(self, ventana):
        # Llama a la función para mostrar la información
        self.mostrar_info(ventana)

        # Actualiza la posición del shooter
        self.moverShooter(ventana)

    def rotarShooter(self, ventana):
        # Calcular el ángulo entre el shooter y la mira
        dx = self.miraX - self.shooter.x
        dy = self.miraY - self.shooter.y
        angulo = math.degrees(math.atan2(-dy, dx))  # -dy porque la coordenada Y crece hacia abajo en la pantalla

        # Rotar la imagen del shooter
        self.shooter_img = pygame.transform.rotate(self.shooter_img_original, angulo - 70)

        # Obtener un nuevo rectángulo para la imagen rotada
        rect = self.shooter_img.get_rect(center=(self.shooter.x + 25, self.shooter.y + 25))

        # Dibujar la imagen rotada en la posición correcta
        ventana.blit(self.shooter_img, rect.topleft)

    def apuntar(self, ventana):
        # Detectar eventos de movimiento del mouse
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                # Obtener la posición del mouse en movimiento
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.miraX, self.miraY = mouse_x, mouse_y

        # Dibujar la mira usando la imagen cargada previamente
        ventana.blit(self.mira_img, (self.miraX - 25, self.miraY - 25))

    def generarZombie(self, ventana):
        if self.tiempo_ultimo_z == 0:
            self.tiempo_ultimo_z = time.time()

        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_ultimo_z

        # Comprobar si ya se ha pasado suficiente tiempo para generar un zombie
        if tiempo_transcurrido >= self.duracion_generacion_z:
            self.tiempo_ultimo_z = tiempo_actual  # Actualizar el tiempo del último zombie generado

            # Crear un nuevo zombie y agregarlo a la lista de zombies
            nuevo_zombie = Zombie(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.shooter.dificultad, self.shooter)
            self.zombies.append(nuevo_zombie)

    def actualizar_zombies(self, ventana):
        for zombie in self.zombies:
            zombie.mover()
            # Eliminar el zombie cuando salga de la pantalla
            if zombie.y > self.SCREEN_HEIGHT:
                self.zombies.remove(zombie)
            # Verificar colisión con el shooter
            if zombie.x < self.shooter.x + 50 and zombie.x + 50 > self.shooter.x and \
            zombie.y < self.shooter.y + 50 and zombie.y + 50 > self.shooter.y:
                self.shooter.recibirDano(zombie.damage)
                self.zombies.remove(zombie)

    def dibujar_zombies(self, ventana):
        for zombie in self.zombies:
            zombie.dibujar(ventana)

    def verificarEstado(self):
        if self.shooter.vida <= 0:
            return False
        else:
            return True

    def iniciar(self):
        pygame.init()

        # Instancia de la ventana
        ventana = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Shooter")

        while self.estado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado = False

            ventana.fill((100, 100, 100))  # Fondo negro

            # Llama a la función para mostrar la información

            self.estado = self.verificarEstado()

            self.generarZombie(ventana)

            self.actualizar_zombies(ventana)

            self.dibujar_zombies(ventana)

            self.mostrar_info(ventana)

            self.apuntar(ventana)

            self.rotarShooter(ventana)

            self.disparar(ventana)

            self.recargar(ventana)

            self.actualizar_balas()

            self.dibujar_balas(ventana)

            self.moverShooter(ventana)

            # Actualiza la ventana para mostrar los cambios
            pygame.display.flip()

        pygame.quit()

        return self.shooter.score