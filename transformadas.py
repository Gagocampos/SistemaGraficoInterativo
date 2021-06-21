import globals
import numpy as np
import math
# Arquivo de funções básicas de transformadas


def translacao(x, y):
    trans_matriz = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [x, y, 1]])
    for pares in globals.shapes[globals.selected].lista:
        pares.coordenadas = np.dot(pares.coordenadas, trans_matriz)


def escalonamento(x, y):
    esc_matriz = np.array([[x, 0, 0],
                           [0, y, 0],
                           [0, 0, 1]])
    centro_x = 0
    centro_y = 0

    for pares in globals.shapes[globals.selected].lista:
        centro_x += pares.coordenadas[0]
        centro_y += pares.coordenadas[1]
    centro_x = centro_x / len(globals.shapes[globals.selected].lista)
    centro_y = centro_y / len(globals.shapes[globals.selected].lista)
    transformation = np.dot(np.array([[1, 0, 0], [0, 1, 0], [-centro_x, -centro_y, 1]]), esc_matriz)
    transformation = np.dot(transformation, np.array([[1, 0, 0], [0, 1, 0], [centro_x, centro_y, 1]]))

    for pares in globals.shapes[globals.selected].lista:
        pares.coordenadas = np.dot(pares.coordenadas, transformation)


def rotacionar(graus, centro, option):
    rotation_matrix = np.array([[math.cos(graus), -math.sin(graus), 0],
                                [math.sin(graus), math.cos(graus), 0],
                                [0, 0, 1]])
    centro_x = 0
    centro_y = 0

    if option == 0:
        for pares in globals.shapes[globals.selected].lista:
            centro_x += pares.coordenadas[0]
            centro_y += pares.coordenadas[1]
        centro_x = centro_x / len(globals.shapes[globals.selected].lista)
        centro_y = centro_y / len(globals.shapes[globals.selected].lista)
    else:
        centro_x = centro.coordenadas[0]
        centro_y = centro.coordenadas[1]
    transformation = np.dot(np.array([[1, 0, 0], [0, 1, 0], [-centro_x, -centro_y, 1]]), rotation_matrix)
    transformation = np.dot(transformation, np.array([[1, 0, 0], [0, 1, 0], [centro_x, centro_y, 1]]))

    for pares in globals.shapes[globals.selected].lista:
        pares.coordenadas = np.dot(pares.coordenadas, transformation)


def translacao3d(x, y, z):
    trans_matriz = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [x, y, z, 1]])

    for segmentos in globals.shapes[globals.selected].lista:
        segmentos[0].coordenadas = np.dot(segmentos[0].coordenadas, trans_matriz)
        segmentos[1].coordenadas = np.dot(segmentos[1].coordenadas, trans_matriz)


def escalonamento3d(x, y, z):
    esc_matriz = np.array([[x, 0, 0, 0],
                           [0, y, 0, 0],
                           [0, 0, z, 0],
                           [0, 0, 0, 1]])
    centro_x = 0
    centro_y = 0
    centro_z = 0
    for segmentos in globals.shapes[globals.selected].lista:
        centro_x += (segmentos[0].coordenadas[0] + segmentos[1].coordenadas[0]) / 2
        centro_y += (segmentos[0].coordenadas[1] + segmentos[1].coordenadas[1]) / 2
        centro_z += (segmentos[0].coordenadas[2] + segmentos[1].coordenadas[2]) / 2

    centro_x = centro_x / len(globals.shapes[globals.selected].lista)
    centro_y = centro_y / len(globals.shapes[globals.selected].lista)
    centro_z = centro_z / len(globals.shapes[globals.selected].lista)
    trans_matriz = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-centro_x, -centro_y, -centro_z, 1]])
    trans_matriz_neg = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [centro_x, centro_y, centro_z, 1]])
    matriz_composta = np.dot(trans_matriz, esc_matriz)
    matriz_composta = np.dot(matriz_composta, trans_matriz_neg)

    for segmentos in globals.shapes[globals.selected].lista:
        segmentos[0].coordenadas = np.dot(segmentos[0].coordenadas, matriz_composta)
        segmentos[1].coordenadas = np.dot(segmentos[1].coordenadas, matriz_composta)

def rotacao3d(angulo, option, vetor):
    # Rotação em torno do eixo x
    if option == 0:
        matriz_rotacao = np.array([[1, 0, 0, 0],
                                   [0, math.cos(angulo), math.sin(angulo), 0],
                                   [0, -math.sin(angulo), math.cos(angulo), 0],
                                   [0, 0, 0, 1]])
        for pares in globals.shapes[globals.selected].lista:
            pares[0].coordenadas = np.dot(pares[0].coordenadas, matriz_rotacao)
            pares[1].coordenadas = np.dot(pares[1].coordenadas, matriz_rotacao)

    # Rotação em torno do eixo y
    elif option == 1:
        matriz_rotacao = np.array([[math.cos(angulo), 0, -math.sin(angulo), 0],
                                   [0, 1, 0, 0],
                                   [math.sin(angulo), 0, math.cos(angulo), 0],
                                   [0, 0, 0, 1]])
        for pares in globals.shapes[globals.selected].lista:
            pares[0].coordenadas = np.dot(pares[0].coordenadas, matriz_rotacao)
            pares[1].coordenadas = np.dot(pares[1].coordenadas, matriz_rotacao)

    # Rotação em torno do eixo z
    elif option == 2:
        matriz_rotacao = np.array([[math.cos(angulo), math.sin(angulo), 0, 0],
                                   [-math.sin(angulo), math.cos(angulo), 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])
        for pares in globals.shapes[globals.selected].lista:
            pares[0].coordenadas = np.dot(pares[0].coordenadas, matriz_rotacao)
            pares[1].coordenadas = np.dot(pares[1].coordenadas, matriz_rotacao)

    # Rotação em torno de um eixo qualquer
    elif option == 3:
        trans_matriz = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [vetor[0].coordenadas[0], vetor[0].coordenadas[1], vetor[0].coordenadas[2], 1]])
        trans_matriz_neg = np.array([[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [-vetor[0].coordenadas[0], -vetor[0].coordenadas[1], -vetor[0].coordenadas[2], 1]])
        hipotenusa = math.sqrt(vetor[1].coordenadas[0] ** 2 + vetor[1].coordenadas[2] ** 2)
        sen_x = vetor[1].coordenadas[2] / hipotenusa
        cos_x = vetor[1].coordenadas[0] / hipotenusa
        rotacao_x = np.array([[1, 0, 0, 0],
                              [0, cos_x, sen_x, 0],
                              [0, -sen_x, cos_x, 0],
                              [0, 0, 0, 1]])

        hipotenusa = math.sqrt(vetor[1].coordenadas[0] ** 2 + vetor[1].coordenadas[1] ** 2)
        sen_z = vetor[1].coordenadas[1] / hipotenusa
        cos_z = vetor[1].coordenadas[0] / hipotenusa
        rotacao_z = np.array([[cos_z, sen_z, 0, 0],
                              [-sen_z, cos_z, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        rotacao_y = np.array([[math.cos(angulo), 0, -math.sin(angulo), 0],
                              [0, 1, 0, 0],
                              [math.sin(angulo), 0, math.cos(angulo), 0],
                              [0, 0, 0, 1]])
        matriz_composta = np.dot(trans_matriz, rotacao_x)
        matriz_composta = np.dot(matriz_composta, rotacao_z)
        matriz_composta = np.dot(matriz_composta, rotacao_y)
        matriz_composta = np.dot(matriz_composta, np.array([[1, 0, 0, 0],
                                                            [0, -cos_x, -sen_x, 0],
                                                            [0, sen_x, -cos_x, 0],
                                                            [0, 0, 0, 1]]))
        matriz_composta = np.dot(matriz_composta, np.array([[-cos_z, -sen_z, 0, 0],
                                                            [sen_z, -cos_z, 0, 0],
                                                            [0, 0, 1, 0],
                                                            [0, 0, 0, 1]]))
        matriz_composta = np.dot(matriz_composta, trans_matriz_neg)

        for segmentos in globals.shapes[globals.selected].lista:
            segmentos[0].coordenadas = np.dot(segmentos[0].coordenadas, matriz_composta)
            segmentos[1].coordenadas = np.dot(segmentos[1].coordenadas, matriz_composta)
