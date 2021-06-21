import numpy as np


# Arquivo de declaração das classes do programa
class Camera:
    def __init__(self, posicao, zoom, angulo):
        self.posicao = posicao
        self.zoom = zoom
        self.angulo = angulo


class Camera3d:
    def __init__(self):
        self.vrp = [0, 0, 0, 1]
        self.paralelo = [5, 5, 1, 1]
        self.distance = 0.2
        self.cop_distance = -0.2


class B_Spline:
    def __init__(self, lista, name):
        self.lista = lista
        self.lista_normalizada = []
        self.name = name


class Curva:
    def __init__(self, lista, name):
        self.lista = lista
        self.lista_normalizada = []
        self.name = name

class Superficie:
    def __init__(self, lista, name):
        self.lista = lista
        self.lista_normalizada = []
        self.lista_final = []
        self.lista_final2 = []
        self.name = name


class Ponto:
    def __init__(self, x, y, code):
        self.coordenadas = np.array([x, y, 1])
        self.code = code


class Ponto3d:
    def __init__(self, x, y, z):
        self.coordenadas = np.array([x, y, z, 1], dtype=object)
        self.code = 0b0000


class Forma3d:
    def __init__(self, name, lista):
        self.lista = lista
        self.name = name
        self.lista_normalizada = []
        self.primeira_lista = []
        self.segunda_lista = []
        self.terceira_lista = []
        self.lista_final = []


class Polygon:
    def __init__(self, name, lista, red, green, blue):
        self.lista = lista
        self.lista_normalizada = []
        self.primeira_lista = []
        self.segunda_lista = []
        self.terceira_lista = []
        self.lista_final = []
        self.name = name
        self.red = red
        self.green = green
        self.blue = blue
