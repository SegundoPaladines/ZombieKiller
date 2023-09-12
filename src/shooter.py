class Shooter:
    def __init__(self, nombre, dificultad):
        if nombre and nombre != "":
            self.nombre = nombre
        else:
            self.nombre = "Guest"

        self.x = 550
        self.y = 280
        self.vida = 100
        self.img = 'img/shooter.png'
        self.dificultad = dificultad
        self.score = 0
        self.municion = None
        
        if dificultad == "Fácil":
            self.municion = 30
        elif dificultad == "Medio":
            self.municion = 25
        elif dificultad == "Difícil":
            self.municion = 20
        elif dificultad == "Infierno":
            self.municion = 10

    def moverDerecha(self):
        if self.dificultad in ["Fácil", "Medio"]:
            self.x = self.x + 10
        elif self.dificultad == "Difícil":
            self.x = self.x + 8
        elif self.dificultad == "Infierno":
            self.x = self.x + 8

    def moverIzquierda(self):
        if self.dificultad in ["Fácil", "Medio"]:
            self.x = self.x - 10
        elif self.dificultad == "Difícil":
            self.x = self.x - 8
        elif self.dificultad == "Infierno":
            self.x = self.x - 8

    def disparar(self):
        if self.municion > 0:
            self.municion = self.municion - 1
            return 0
        else:
            return self.recargar()

    def recargar(self):
        if self.dificultad == "Fácil":
            self.municion = 30
        elif self.dificultad == "Medio":
            self.municion = 25
        elif self.dificultad == "Difícil":
            self.municion = 20
        elif self.dificultad == "Infierno":
            self.municion = 10
    
    def tiempoRecarga(self):
        if self.dificultad == "Fácil":
            return 1
        elif self.dificultad == "Medio":
            return 2
        elif self.dificultad == "Difícil":
            return 3
        elif self.dificultad == "Infierno":
            return 4

    def estado(self):
        estado_shooter = {
            "nombre": self.nombre,
            "x": self.x,
            "y": self.y,
            "vida": self.vida,
            "dificultad": self.dificultad,
            "score": self.score,
            "municion": self.municion
        }
        return estado_shooter
    
    def recibirDano(self, cantidad):
        self.vida -= cantidad