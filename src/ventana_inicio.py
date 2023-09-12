import pygame
import time

class VentanaInicio:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Constantes
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 600

        self.inicio_sound = pygame.mixer.Sound("sound/inicio.mp3")
        self.sound_timer = time.time()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT = pygame.font.Font(None, 36)

        # Inicialización de la pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zoombie Shooter")

        # Cargar la imagen de fondo
        self.fondo = pygame.image.load('img/fondo.jpg')
        self.fondo = pygame.transform.scale(self.fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Campo de entrada de texto
        self.input_text = ""
        self.input_rect = pygame.Rect(400, 200, 400, 40)
        self.input_color = pygame.Color(self.BLACK)
        self.input_active = False

        # Variables para los botones de dificultad
        self.dificultades = ["Fácil", "Medio", "Difícil", "Infierno"]
        self.selected_difficulty = "Fácil"
        self.button_font = pygame.font.Font(None, 32)
        self.buttons = []

        # Almacenar la entrada del usuario
        self.entrada = None

        # Bandera para cerrar la ventana
        self.cerrar_ventana = False

    # Función para manejar el campo de entrada de texto
    def control_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    # Realiza alguna acción con el texto ingresado (por ejemplo, almacenarlo en 'nombre')
                    self.nombre = self.input_text
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hizo clic en el campo de entrada de texto
            if self.input_rect.collidepoint(event.pos):
                self.input_active = not self.input_active
            else:
                self.input_active = False

    # Función para manejar los eventos de los botones de dificultad
    def handle_button_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, difficulty in self.buttons:
                if button.collidepoint(event.pos):
                    self.selected_difficulty = difficulty

    # Función para crear botones de dificultad
    def create_difficulty_buttons(self):
        button_width, button_height = 200, 50
        x, y = 200, 300

        for difficulty in self.dificultades:
            button_rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append((button_rect, difficulty))
            x += button_width + 20

    # Función para mostrar los botones de dificultad
    def draw_difficulty_buttons(self):
        for button, difficulty in self.buttons:
            if self.selected_difficulty == difficulty:
                color = (255, 0, 0)  # Rojo para el botón seleccionado
            else:
                color = self.BLACK

            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, self.WHITE, button, 2)

            text = self.button_font.render(difficulty, True, self.WHITE if color != self.WHITE else self.BLACK)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)

    def repetirSonido(self):
        if (time.time() - self.sound_timer) >= 86:
            self.inicio_sound.play()
            self.sound_timer = time.time()

    # Función para mostrar la pantalla de inicio
    def mostrar_pantalla_inicio(self):
        self.create_difficulty_buttons()

        self.inicio_sound.play()
        
        while not self.cerrar_ventana:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.control_input(event)
                self.handle_button_events(event)

            self.screen.blit(self.fondo, (0, 0))
            self.mostrar_mensaje("Bienvenido al juego", 450, 40)
            self.mostrar_mensaje("Ingrese su Nombre:", 400, 160)

            pygame.draw.rect(self.screen, self.input_color, self.input_rect, 2)
            text_surface = self.FONT.render(self.input_text, True, self.WHITE)
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

            self.draw_difficulty_buttons()

            self.repetirSonido()

            if self.selected_difficulty:
                self.mostrar_mensaje(f"Dificultad seleccionada: {self.selected_difficulty}", 450, 400)
            
            self.mostrar_mensaje("Presiona Enter Para Comenzar a Jugar", 350, 500)

            pygame.display.update()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.input_text:
                    self.entrada = (self.input_text, self.selected_difficulty)
                else:
                    self.entrada = ("Guest", self.selected_difficulty)
                self.cerrar_ventana = True

            # Verificar si el usuario presionó Enter y devolver los datos
            if self.entrada:
                self.inicio_sound.stop()
                return self.entrada

    # Función para mostrar un mensaje en pantalla
    def mostrar_mensaje(self, texto, x, y):
        mensaje = self.FONT.render(texto, True, self.WHITE)
        self.screen.blit(mensaje, (x, y))