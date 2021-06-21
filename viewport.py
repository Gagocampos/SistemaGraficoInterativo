import globals
import math
from classes import *
import cairo
import clipping

surface = None


# Função principal de desenho dos polígonos
def desenhar():
    cr = cairo.Context(surface)
    x = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    y = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for formas in globals.shapes:
        if isinstance(formas, Polygon):
            if formas.lista_final:
                cr.move_to(formas.lista_final[0].coordenadas[0] * x + 20,
                           formas.lista_final[0].coordenadas[1] * y + 20)
                for pontos in formas.lista_final:
                    cr.line_to(pontos.coordenadas[0] * x + 20, pontos.coordenadas[1] * y + 20)
                cr.set_source_rgb(formas.red, formas.green, formas.blue)
                cr.stroke()
    globals.window.queue_draw()


# Função que desenha curvas conforme o método de Bezier
def desenhar_curvas():
    matriz_bezier = np.array([[-1, 3, -3, 1],
                              [3, -6, 3, 0],
                              [-3, 3, 0, 0],
                              [1, 0, 0, 0]])
    cr = cairo.Context(surface)
    x = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    y = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for objetos in globals.shapes:
        if isinstance(objetos, Curva):
            cr.move_to(objetos.lista_normalizada[0].coordenadas[0] * x + 20,
                       objetos.lista_normalizada[0].coordenadas[1] * y + 20)
            for i in range(int(len(objetos.lista_normalizada) / 4)):
                geometria_x = np.array([[objetos.lista_normalizada[4*i].coordenadas[0]],
                                        [objetos.lista_normalizada[4*i + 1].coordenadas[0]],
                                        [objetos.lista_normalizada[4*i + 2].coordenadas[0]],
                                        [objetos.lista_normalizada[4*i + 3].coordenadas[0]]])
                geometria_y = np.array([[objetos.lista_normalizada[4*i].coordenadas[1]],
                                        [objetos.lista_normalizada[4*i + 1].coordenadas[1]],
                                        [objetos.lista_normalizada[4*i + 2].coordenadas[1]],
                                        [objetos.lista_normalizada[4*i + 3].coordenadas[1]]])

                for n in range(100):
                    matriz_t = np.array([(n / 100) ** 3, (n / 100) ** 2, (n / 100), 1])
                    tb = np.dot(matriz_t, matriz_bezier)
                    xt = np.dot(tb, geometria_x)
                    yt = np.dot(tb, geometria_y)
                    if 0 <= xt <= 2 and 0 <= yt <= 2:
                        cr.line_to(xt * x + 20, yt * y + 20)
                    else:
                        cr.move_to(xt * x + 20, yt * y + 20)
            cr.stroke()
    globals.window.queue_draw()


# Função que desenha superficies bicubicas de Bezier por Blending Functions
def superficies_bicubicas():
    matriz_bezier = np.array([[-1, 3, -3, 1],
                              [3, -6, 3, 0],
                              [-3, 3, 0, 0],
                              [1, 0, 0, 0]])
    trans_matriz = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-1, -1, -globals.camera3d.cop_distance, 1]])
    cr = cairo.Context(surface)
    x = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    y = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for objetos in globals.shapes:
        if isinstance(objetos, Superficie):
            n = objetos.lista_normalizada
            matriz_geometria_x = np.array(
                [[n[0].coordenadas[0], n[1].coordenadas[0], n[2].coordenadas[0], n[3].coordenadas[0]],
                 [n[4].coordenadas[0], n[5].coordenadas[0], n[6].coordenadas[0], n[7].coordenadas[0]],
                 [n[8].coordenadas[0], n[9].coordenadas[0], n[10].coordenadas[0], n[11].coordenadas[0]],
                 [n[12].coordenadas[0], n[13].coordenadas[0], n[14].coordenadas[0], n[15].coordenadas[0]]])
            matriz_geometria_y = np.array(
                [[n[0].coordenadas[1], n[1].coordenadas[1], n[2].coordenadas[1], n[3].coordenadas[1]],
                 [n[4].coordenadas[1], n[5].coordenadas[1], n[6].coordenadas[1], n[7].coordenadas[1]],
                 [n[8].coordenadas[1], n[9].coordenadas[1], n[10].coordenadas[1], n[11].coordenadas[1]],
                 [n[12].coordenadas[1], n[13].coordenadas[1], n[14].coordenadas[1], n[15].coordenadas[1]]])
            matriz_geometria_z = np.array(
                [[n[0].coordenadas[2], n[1].coordenadas[2], n[2].coordenadas[2], n[3].coordenadas[2]],
                 [n[4].coordenadas[2], n[5].coordenadas[2], n[6].coordenadas[2], n[7].coordenadas[2]],
                 [n[8].coordenadas[2], n[9].coordenadas[2], n[10].coordenadas[2], n[11].coordenadas[2]],
                 [n[12].coordenadas[2], n[13].coordenadas[2], n[14].coordenadas[2], n[15].coordenadas[2]]])
            composta_x = np.dot(matriz_bezier, matriz_geometria_x)
            composta_x = np.dot(composta_x, matriz_bezier.transpose())
            composta_y = np.dot(matriz_bezier, matriz_geometria_y)
            composta_y = np.dot(composta_y, matriz_bezier.transpose())
            composta_z = np.dot(matriz_bezier, matriz_geometria_z)
            composta_z = np.dot(composta_z, matriz_bezier.transpose())

            for t in range(100):
                matriz_t = np.array([[(t/100)**3], [(t/100)**2], [t/100], [1]])
                for s in range(100):
                    matriz_s = np.array([(s/100)**3, (s/100)**2, s/100, 1])
                    escalar_x = np.dot(matriz_s, composta_x)
                    escalar_x = np.dot(escalar_x, matriz_t)
                    escalar_y = np.dot(matriz_s, composta_y)
                    escalar_y = np.dot(escalar_y, matriz_t)
                    escalar_z = np.dot(matriz_s, composta_z)
                    escalar_z = np.dot(escalar_z, matriz_t)
                    objetos.lista_final.append(Ponto3d(escalar_x, escalar_y, escalar_z))

            for s in range(100):
                matriz_s = np.array([(s / 100) ** 3, (s / 100) ** 2, s / 100, 1])
                for t in range(100):
                    matriz_t = np.array([[(t / 100) ** 3], [(t / 100) ** 2], [t / 100], [1]])
                    escalar_x = np.dot(matriz_s, composta_x)
                    escalar_x = np.dot(escalar_x, matriz_t)
                    escalar_y = np.dot(matriz_s, composta_y)
                    escalar_y = np.dot(escalar_y, matriz_t)
                    escalar_z = np.dot(matriz_s, composta_z)
                    escalar_z = np.dot(escalar_z, matriz_t)
                    objetos.lista_final2.append(Ponto3d(escalar_x, escalar_y, escalar_z))

            for i in range(100):
                objetos.lista_final[i*100].coordenadas = np.dot(objetos.lista_final[i*100].coordenadas, trans_matriz)
                cr.move_to((objetos.lista_final[i*100].coordenadas[0] * x * globals.camera3d.distance /objetos.lista_final[i*100].coordenadas[2] + x),
                           (objetos.lista_final[i*100].coordenadas[1] * y * globals.camera3d.distance /objetos.lista_final[i*100].coordenadas[2] + y))
                for n in range(99):
                    objetos.lista_final[i*100+(n+1)].coordenadas = np.dot(objetos.lista_final[i*100+n+1].coordenadas, trans_matriz)
                    if -1 < objetos.lista_final[i*100+n+1].coordenadas[0] < 1 and -1 < objetos.lista_final[i*100+n+1].coordenadas[0] < 1:
                        cr.line_to((objetos.lista_final[i*100+n+1].coordenadas[0] * x * globals.camera3d.distance /objetos.lista_final[i*100+n+1].coordenadas[2] + x),
                                    (objetos.lista_final[i*100+n+1].coordenadas[1] * y * globals.camera3d.distance /objetos.lista_final[i*100+n+1].coordenadas[2] + y))
                    else:
                        cr.move_to((objetos.lista_final[i * 100 + n + 1].coordenadas[
                                        0] * x * globals.camera3d.distance /
                                    objetos.lista_final[i * 100 + n + 1].coordenadas[2] + x),
                                   (objetos.lista_final[i * 100 + n + 1].coordenadas[
                                        1] * y * globals.camera3d.distance /
                                    objetos.lista_final[i * 100 + n + 1].coordenadas[2] + y))
            cr.stroke()

            for i in range(100):
                objetos.lista_final2[i*100].coordenadas = np.dot(objetos.lista_final2[i*100].coordenadas, trans_matriz)
                cr.move_to((objetos.lista_final2[i*100].coordenadas[0] * x * globals.camera3d.distance /objetos.lista_final2[i*100].coordenadas[2] + x),
                           (objetos.lista_final2[i*100].coordenadas[1] * y * globals.camera3d.distance /objetos.lista_final2[i*100].coordenadas[2] + y))
                for n in range(99):
                    objetos.lista_final2[i*100+(n+1)].coordenadas = np.dot(objetos.lista_final2[i*100+n+1].coordenadas, trans_matriz)
                    if -1 < objetos.lista_final2[i * 100 + n + 1].coordenadas[0] < 1 and -1 < objetos.lista_final2[i * 100 + n + 1].coordenadas[0] < 1:
                        cr.line_to((objetos.lista_final2[i*100+n+1].coordenadas[0] * x * globals.camera3d.distance /objetos.lista_final2[i*100+n+1].coordenadas[2] + x),
                                    (objetos.lista_final2[i*100+n+1].coordenadas[1] * y * globals.camera3d.distance /objetos.lista_final2[i*100+n+1].coordenadas[2] + y))
                    else:
                        cr.move_to((objetos.lista_final2[i * 100 + n + 1].coordenadas[
                                        0] * x * globals.camera3d.distance /
                                    objetos.lista_final2[i * 100 + n + 1].coordenadas[2] + x),
                                   (objetos.lista_final2[i * 100 + n + 1].coordenadas[
                                        1] * y * globals.camera3d.distance /
                                    objetos.lista_final2[i * 100 + n + 1].coordenadas[2] + y))
            cr.stroke()

    globals.window.queue_draw()


# Função que desenha B-Splines usando diferenças adiante
def fwd_diff():
    matriz_spline = np.array([[-1/6, 3/6, -3/6, 1/6],
                              [3/6, -1, 3/6, 0],
                              [-3/6, 0, 3/6, 0],
                              [1/6, 4/6, 1/6, 0]])
    delta = np.array([[0, 0, 0, 1],
                      [0.01 ** 3, 0.01 ** 2, 0.01, 0],
                      [6 * 0.01 ** 3, 2 * 0.01 ** 2, 0, 0],
                      [6 * 0.01 ** 3, 0, 0, 0]])
    cr = cairo.Context(surface)
    width = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    height = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for objetos in globals.shapes:
        if isinstance(objetos, B_Spline):
            for i in range(len(objetos.lista_normalizada) - 3):
                cx = np.array([[objetos.lista_normalizada[0 + i].coordenadas[0]],
                              [objetos.lista_normalizada[1 + i].coordenadas[0]],
                              [objetos.lista_normalizada[2 + i].coordenadas[0]],
                              [objetos.lista_normalizada[3 + i].coordenadas[0]]])
                cx = np.dot(matriz_spline, cx)
                cx = np.dot(delta, cx)
                cy = np.array([[objetos.lista_normalizada[0 + i].coordenadas[1]],
                               [objetos.lista_normalizada[1 + i].coordenadas[1]],
                               [objetos.lista_normalizada[2 + i].coordenadas[1]],
                               [objetos.lista_normalizada[3 + i].coordenadas[1]]])
                cy = np.dot(matriz_spline, cy)
                cy = np.dot(delta, cy)
                x = cx[0][0]
                y = cy[0][0]
                cr.move_to(x * width + 20, y * height + 20)
                for n in range(100):
                    x = x + cx[1][0]
                    cx[1][0] = cx[1][0] + cx[2][0]
                    cx[2][0] = cx[2][0] + cx[3][0]
                    y = y + cy[1][0]
                    cy[1][0] = cy[1][0] + cy[2][0]
                    cy[2][0] = cy[2][0] + cy[3][0]
                    if 0 <= x <= 2 and 0 <= y <= 2:
                        cr.line_to(x * width + 20, y * height + 20)
                    else:
                        cr.move_to(x * width + 20, y * height + 20)
            cr.stroke()
    globals.window.queue_draw()


# Desenha uma superfície bicúbica B-Spline com diferenças adiante
def surface_fwd_diff():
    matriz_spline = np.array([[-1 / 6, 3 / 6, -3 / 6, 1 / 6],
                              [3 / 6, -1, 3 / 6, 0],
                              [-3 / 6, 0, 3 / 6, 0],
                              [1 / 6, 4 / 6, 1 / 6, 0]])
    delta_s = np.array([[0, 0, 0, 1],
                      [0.02 ** 3, 0.02 ** 2, 0.02, 0],
                      [6 * 0.02 ** 3, 2 * 0.02 ** 2, 0, 0],
                      [6 * 0.02 ** 3, 0, 0, 0]])
    trans_matriz = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-1, -1, -globals.camera3d.cop_distance, 1]])
    delta_t = delta_s.transpose()

    cr = cairo.Context(surface)
    width = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    height = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for objetos in globals.shapes:
        if isinstance(objetos, Superficie):
            n = objetos.lista_normalizada
            matriz_geometria_x = np.array(
                [[n[0].coordenadas[0], n[1].coordenadas[0], n[2].coordenadas[0], n[3].coordenadas[0]],
                 [n[4].coordenadas[0], n[5].coordenadas[0], n[6].coordenadas[0], n[7].coordenadas[0]],
                 [n[8].coordenadas[0], n[9].coordenadas[0], n[10].coordenadas[0], n[11].coordenadas[0]],
                 [n[12].coordenadas[0], n[13].coordenadas[0], n[14].coordenadas[0], n[15].coordenadas[0]]])
            matriz_geometria_y = np.array(
                [[n[0].coordenadas[1], n[1].coordenadas[1], n[2].coordenadas[1], n[3].coordenadas[1]],
                 [n[4].coordenadas[1], n[5].coordenadas[1], n[6].coordenadas[1], n[7].coordenadas[1]],
                 [n[8].coordenadas[1], n[9].coordenadas[1], n[10].coordenadas[1], n[11].coordenadas[1]],
                 [n[12].coordenadas[1], n[13].coordenadas[1], n[14].coordenadas[1], n[15].coordenadas[1]]])
            matriz_geometria_z = np.array(
                [[n[0].coordenadas[2], n[1].coordenadas[2], n[2].coordenadas[2], n[3].coordenadas[2]],
                 [n[4].coordenadas[2], n[5].coordenadas[2], n[6].coordenadas[2], n[7].coordenadas[2]],
                 [n[8].coordenadas[2], n[9].coordenadas[2], n[10].coordenadas[2], n[11].coordenadas[2]],
                 [n[12].coordenadas[2], n[13].coordenadas[2], n[14].coordenadas[2], n[15].coordenadas[2]]])
            cx = np.dot(matriz_spline, matriz_geometria_x)
            cx = np.dot(cx, np.transpose(matriz_spline))
            cy = np.dot(matriz_spline, matriz_geometria_y)
            cy = np.dot(cy, np.transpose(matriz_spline))
            cz = np.dot(matriz_spline, matriz_geometria_z)
            cz = np.dot(cz, np.transpose(matriz_spline))

            ddx = np.dot(delta_s, cx)
            ddx = np.dot(ddx, delta_t)
            ddy = np.dot(delta_s, cy)
            ddy = np.dot(ddy, delta_t)
            ddz = np.dot(delta_s, cz)
            ddz = np.dot(ddz, delta_t)

            for n in range(51):
                x = ddx[0][0]
                x1 = ddx[0][1]
                x2 = ddx[0][2]
                x3 = ddx[0][3]
                y = ddy[0][0]
                y1 = ddy[0][1]
                y2 = ddy[0][2]
                y3 = ddy[0][3]
                z = ddz[0][0]
                z1 = ddz[0][1]
                z2 = ddz[0][2]
                z3 = ddz[0][3]
                for n in range(50):
                    x = x + x1
                    x1 = x1 + x2
                    x2 = x2 + x3
                    y = y + y1
                    y1 = y1 + y2
                    y2 = y2 + y3
                    z = z + z1
                    z1 = z1 + z2
                    z2 = z2 + z3
                    objetos.lista_final.append(Ponto3d(x, y, z))
                ddx[0] = ddx[0] + ddx[1]
                ddx[1] = ddx[1] + ddx[2]
                ddx[2] = ddx[2] + ddx[3]
                ddy[0] = ddy[0] + ddy[1]
                ddy[1] = ddy[1] + ddy[2]
                ddy[2] = ddy[2] + ddy[3]
                ddz[0] = ddz[0] + ddz[1]
                ddz[1] = ddz[1] + ddz[2]
                ddz[2] = ddz[2] + ddz[3]

            ddx = np.dot(delta_s, cx)
            ddx = np.transpose(np.dot(ddx, delta_t))
            ddy = np.dot(delta_s, cy)
            ddy = np.transpose(np.dot(ddy, delta_t))
            ddz = np.dot(delta_s, cz)
            ddz = np.transpose(np.dot(ddz, delta_t))

            for n in range(51):
                x = ddx[0][0]
                x1 = ddx[0][1]
                x2 = ddx[0][2]
                x3 = ddx[0][3]
                y = ddy[0][0]
                y1 = ddy[0][1]
                y2 = ddy[0][2]
                y3 = ddy[0][3]
                z = ddz[0][0]
                z1 = ddz[0][1]
                z2 = ddz[0][2]
                z3 = ddz[0][3]
                for n in range(50):
                    x = x + x1
                    x1 = x1 + x2
                    x2 = x2 + x3
                    y = y + y1
                    y1 = y1 + y2
                    y2 = y2 + y3
                    z = z + z1
                    z1 = z1 + z2
                    z2 = z2 + z3
                    objetos.lista_final.append(Ponto3d(x, y, z))
                ddx[0] = ddx[0] + ddx[1]
                ddx[1] = ddx[1] + ddx[2]
                ddx[2] = ddx[2] + ddx[3]
                ddy[0] = ddy[0] + ddy[1]
                ddy[1] = ddy[1] + ddy[2]
                ddy[2] = ddy[2] + ddy[3]
                ddz[0] = ddz[0] + ddz[1]
                ddz[1] = ddz[1] + ddz[2]
                ddz[2] = ddz[2] + ddz[3]

            for n in range(len(objetos.lista_final) - 1):
                if (n) % 50 == 0:
                    objetos.lista_final[n].coordenadas = np.dot(objetos.lista_final[n].coordenadas, trans_matriz)
                    cr.move_to((objetos.lista_final[n].coordenadas[0] * width * globals.camera3d.distance /
                                objetos.lista_final[n].coordenadas[2] + width),
                               (objetos.lista_final[n].coordenadas[1] * height * globals.camera3d.distance /
                                objetos.lista_final[n].coordenadas[2] + height))
                else:
                    objetos.lista_final[n].coordenadas = np.dot(objetos.lista_final[n].coordenadas, trans_matriz)
                    cr.line_to((objetos.lista_final[n].coordenadas[0] * width * globals.camera3d.distance /
                                objetos.lista_final[n].coordenadas[2] + width),
                               (objetos.lista_final[n].coordenadas[1] * height * globals.camera3d.distance /
                                objetos.lista_final[n].coordenadas[2] + height))
            cr.stroke()

    globals.window.queue_draw()



# Função que desenha as formas tridimensionais com uma projeção
# paralela
def desenho3d():
    width = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    height = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2
    trans_matriz = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [-globals.camera3d.vrp[0], -globals.camera3d.vrp[1], -globals.camera3d.vrp[2], 1]])
    hipotenusa = math.sqrt(globals.camera3d.paralelo[2] ** 2 + globals.camera3d.paralelo[0] ** 2)
    seno_x = globals.camera3d.paralelo[2] / hipotenusa
    cos_x = globals.camera3d.paralelo[0] / hipotenusa
    hipotenusa = math.sqrt(globals.camera3d.paralelo[2]**2 + globals.camera3d.paralelo[1]**2)
    seno_y = globals.camera3d.paralelo[2] / hipotenusa
    cos_y = globals.camera3d.paralelo[1] / hipotenusa
    matriz_rotacao_x = np.array([[1, 0, 0, 0],
                                 [0, cos_x, seno_x, 0],
                                 [0, -seno_x, cos_x, 0],
                                 [0, 0, 0, 1]])
    matriz_rotacao_y = np.array([[cos_y, 0, -seno_y, 0],
                                 [0, 1, 0, 0],
                                 [seno_y, 0, cos_y, 0],
                                 [0, 0, 0, 1]])
    matriz_composta = np.dot(trans_matriz, matriz_rotacao_x)
    matriz_composta = np.dot(matriz_composta, matriz_rotacao_y)
    cr = cairo.Context(surface)

    for objetos in globals.shapes:
        if isinstance(objetos, Forma3d):
            for segmentos in objetos.lista_normalizada:
                segmentos[0].coordenadas[2] = segmentos[0].coordenadas[2] * 400 / 20
                segmentos[1].coordenadas[2] = segmentos[1].coordenadas[2] * 400 / 20
                segmentos[0].coordenadas = np.dot(segmentos[0].coordenadas, matriz_composta)
                segmentos[0].code = clipping.codificar(segmentos[0].coordenadas[0], segmentos[0].coordenadas[1])
                segmentos[1].coordenadas = np.dot(segmentos[1].coordenadas, matriz_composta)
                segmentos[1].code = clipping.codificar(segmentos[1].coordenadas[0], segmentos[1].coordenadas[1])

    clipping.sutherland_hodgeman3d()
    for objetos in globals.shapes:
        if isinstance(objetos, Forma3d):
            for segmentos in objetos.lista_final:
                cr.move_to(segmentos[0].coordenadas[0] * width + 20, segmentos[0].coordenadas[1] * height + 20)
                cr.line_to(segmentos[1].coordenadas[0] * width + 20, segmentos[1].coordenadas[1] * height + 20)
            cr.stroke()

    globals.window.queue_draw()


# Função que desenha as formas tridimensionais com uma projeção
# em perspectiva
def desenho_perspectiva():
    width = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    height = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2
    trans_matriz = np.array([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [-1, -1, -globals.camera3d.cop_distance, 1]])
    cr = cairo.Context(surface)

    for objetos in globals.shapes:
        if isinstance(objetos, Forma3d):
            for segmentos in objetos.lista_normalizada:
                segmentos[0].coordenadas = np.dot(segmentos[0].coordenadas, trans_matriz)
                segmentos[1].coordenadas = np.dot(segmentos[1].coordenadas, trans_matriz)
                segmentos[0].coordenadas[0] = (segmentos[0].coordenadas[0] * width * globals.camera3d.distance /
                                               segmentos[0].coordenadas[2] + width) / width
                segmentos[0].coordenadas[1] = (segmentos[0].coordenadas[1] * height * globals.camera3d.distance /
                                               segmentos[0].coordenadas[2] + height) / height
                segmentos[0].code = clipping.codificar(segmentos[0].coordenadas[0], segmentos[0].coordenadas[1])
                segmentos[1].coordenadas[0] = (segmentos[1].coordenadas[0] * width * globals.camera3d.distance /
                                               segmentos[1].coordenadas[2] + width) / width
                segmentos[1].coordenadas[1] = (segmentos[1].coordenadas[1] * height * globals.camera3d.distance /
                                               segmentos[1].coordenadas[2] + height) / height
                segmentos[1].code = clipping.codificar(segmentos[1].coordenadas[0], segmentos[1].coordenadas[1])

    clipping.sutherland_hodgeman3d()
    for objetos in globals.shapes:
        if isinstance(objetos, Forma3d):
            for segmentos in objetos.lista_final:
                cr.move_to(segmentos[0].coordenadas[0] * width + 20, segmentos[0].coordenadas[1] * height + 20)
                cr.line_to(segmentos[1].coordenadas[0] * width + 20, segmentos[1].coordenadas[1] * height + 20)
            cr.stroke()
    globals.window.queue_draw()


# Função chamada sempre que uma nova forma é inserida pelo usuário
# que leva a origem dos eixos para o centro da tela
def ajustar_coordenadas():
    matriz_de_ajuste = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() / 2) - 20,
                                  float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() / 2) - 20, 1]])

    for pares in globals.shapes[len(globals.shapes) - 1].lista:
        pares.coordenadas = np.dot(pares.coordenadas, matriz_de_ajuste)


# Função que transforma as coordenadas do mundo em coordenadas normalizadas
# e as armazena em uma nova lista
def normalizar_coordenadas():
    largura = float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 40) / 2
    altura = float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 40) / 2

    for formas in globals.shapes:
        formas.lista_normalizada.clear()
        if isinstance(formas, Forma3d):
            for segmentos in formas.lista:
                coord1 = Ponto3d(segmentos[0].coordenadas[0] / largura,
                                 segmentos[0].coordenadas[1] / altura, segmentos[0].coordenadas[2] / 400)
                coord2 = Ponto3d(segmentos[1].coordenadas[0] / largura,
                                 segmentos[1].coordenadas[1] / altura, segmentos[1].coordenadas[2] / 400)
                formas.lista_normalizada.append([coord1, coord2])
        elif isinstance(formas, Superficie):
            formas.lista_final.clear()
            formas.lista_final2.clear()
            for pontos in formas.lista:
                coord = Ponto3d(pontos.coordenadas[0] / largura,
                                 pontos.coordenadas[1] / altura, pontos.coordenadas[2] / 400)
                formas.lista_normalizada.append(coord)
        else:
            for pares in formas.lista:
                x = pares.coordenadas[0] / largura
                y = pares.coordenadas[1] / altura
                coord = Ponto(x, y, clipping.codificar(x, y))
                formas.lista_normalizada.append(coord)


# Função responsável por realizar as transformadas sobre a matriz
# normalizada a fim de gerar as coordenadas finais de visualização
# do usuário, com auxílio da variável "camera"
def reajustar_camera():
    x = globals.camera.posicao[0] / (globals.gtkBuilder.get_object('drawing1').get_allocated_width() / 2 - 20)
    y = globals.camera.posicao[1] / (globals.gtkBuilder.get_object('drawing1').get_allocated_height() / 2 - 20)
    matriz_translacao = np.array([[1, 0, 0],
                                  [0, 1, 0],
                                  [x, y, 1]])
    matriz_zoom = np.array([[globals.camera.zoom, 0, 0],
                            [0, globals.camera.zoom, 0],
                            [0, 0, 1]])
    matriz_rotacao = np.array([[math.cos(globals.camera.angulo), -math.sin(globals.camera.angulo), 0],
                               [math.sin(globals.camera.angulo), math.cos(globals.camera.angulo), 0],
                               [0, 0, 1]])

    matriz_composta = np.dot(np.array([[1, 0, 0], [0, 1, 0], [-1, -1, 1]]), matriz_zoom)
    matriz_composta = np.dot(matriz_composta, matriz_rotacao)
    matriz_composta = np.dot(matriz_composta, np.array([[1, 0, 0], [0, 1, 0], [1, 1, 1]]))
    matriz_composta = np.dot(matriz_composta, matriz_translacao)
    
    for formas in globals.shapes:
        if not isinstance(formas, Forma3d) and not isinstance(formas, Superficie):
            for pares in formas.lista_normalizada:
                pares.coordenadas = np.dot(pares.coordenadas, matriz_composta)
                pares.code = clipping.codificar(pares.coordenadas[0], pares.coordenadas[1])

    clipping.sutherland_hodgeman()


# Clear the surface, removing the scribbles
def clear_surface():
    global surface
    cr = cairo.Context(surface)
    cr.set_source_rgb(1, 1, 1)
    cr.paint()
    del cr


# Creates the surface
def configure_event_cb(wid, evt):
    global surface
    if surface is not None:
        del surface
        surface = None
    win = wid.get_window()
    width = wid.get_allocated_width()
    height = wid.get_allocated_height()
    surface = win.create_similar_surface(
        cairo.CONTENT_COLOR,
        width,
        height)
    clear_surface()
    return True


# Redraw the screen from the surface
def draw_cb(wid, cr):
    global surface
    cr.set_source_surface(surface, 0, 0)
    cr.paint()
    return False


# Função que simplesmente desenha uma borda na DrawingArea
# com espaçamento de 20 unidades
def desenhar_borda():
    cr = cairo.Context(surface)
    cr.move_to(20, 20)
    cr.line_to(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 20, 20)
    cr.line_to(globals.gtkBuilder.get_object('drawing1').get_allocated_width() - 20,
               globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 20)
    cr.line_to(20, globals.gtkBuilder.get_object('drawing1').get_allocated_height() - 20)
    cr.line_to(20, 20)
    cr.set_line_width(2)
    cr.set_source_rgb(0, 0, 0)
    cr.stroke()
    globals.window.queue_draw()


# Função que é chamada toda vez que ocorre um modificação por parte
# do usuário
def redesenhar():
    clear_surface()
    desenhar_borda()
    normalizar_coordenadas()
    reajustar_camera()
    desenhar()
    desenhar_curvas()
    fwd_diff()
    if globals.gtkBuilder.get_object('spline_check').get_active():
        surface_fwd_diff()
    else:
        superficies_bicubicas()
    if globals.gtkBuilder.get_object('paralela').get_active():
        desenho3d()
    else:
        desenho_perspectiva()
