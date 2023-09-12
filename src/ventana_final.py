import pygame
import sys
import time

class VentanaFinal:
    def __init__(self, score):
        self.score = score

        pygame.mixer.init()

        self.inicio_sound = pygame.mixer.Sound("sound/inicio.mp3")
        self.final_sound = pygame.mixer.Sound("sound/final.mp3")
        self.sound_timer = time.time()


    def reiniciar(self):
        pygame.init()

        pantalla = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Game Over")

        self.final_sound.play()
        self.inicio_sound.play()

        font = pygame.font.Font(None, 70)
        texto_score = font.render(f"Has muerto, tu score es: {self.score}", True, (255, 0, 0))
        texto_enter = font.render("Presiona ENTER para reiniciar", True, (255, 0, 0))
        fondo = pygame.image.load("img/final.jpg")
        fondo = pygame.transform.scale(fondo, (1200, 600))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        return True  # El usuario presionó ENTER para reiniciar

            pantalla.blit(fondo, (0, 0))
            pantalla.blit(texto_score, (200, 200))
            pantalla.blit(texto_enter, (200, 300))
            pygame.display.update()

        self.final_sound.stop()
        self.inicio_sound.stop()