import pygame
from ventana_inicio import VentanaInicio
from shooter import Shooter
from juego import Juego
from ventana_final import VentanaFinal

def inicio():
    ventana_inicio = VentanaInicio()
    entrada = ventana_inicio.mostrar_pantalla_inicio()
    nombre, dificultad = entrada
    
    shooter = Shooter(nombre, dificultad)

    juego = Juego(shooter)
    score = juego.iniciar()
    
    ventana_final = VentanaFinal(score)
    reiniciar = ventana_final.reiniciar()

    if  reiniciar == True:
       inicio()
 
if __name__ == "__main__":
    inicio()