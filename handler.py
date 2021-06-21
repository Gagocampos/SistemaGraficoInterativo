import transformadas
import viewport
import globals
import classes
import filereader


# Arquivo contendo a classe Handler responsável por tratar
# sinais e botões da interface gráfica

class Handler:

    def spline_check_toggled_cb(self, btn):
        viewport.redesenhar()

    def abrir_arquivo_activate_cb(self, btn):
        globals.gtkBuilder.get_object('file_chooser').present()

    def file_ok_clicked_cb(self, btn):
        arquivo = globals.gtkBuilder.get_object('file_chooser').get_filename()
        filereader.read_object(arquivo)
        globals.gtkBuilder.get_object('file_chooser').hide()
        viewport.redesenhar()

    def cancelar_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('file_chooser').hide()

    def paralela_toggled_cb(self, btn):
        globals.gtkBuilder.get_object('perspectiva').set_active(False)
        viewport.redesenhar()

    def perspectiva_toggled_cb(self, btn):
        globals.gtkBuilder.get_object('paralela').set_active(False)
        viewport.redesenhar()

    def inserir_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('polygon_name').set_text('')
        globals.gtkBuilder.get_object('curva_name').set_text('')
        globals.gtkBuilder.get_object('dialogue').present()

    def shape3d_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('dialogue').hide()
        globals.gtkBuilder.get_object('name3d_window').present()

    def name3d_ok_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('name3d_window').hide()
        globals.gtkBuilder.get_object('dados3d_window').present()

    def mais_segmentos_clicked_cb(self, btn):
        globals.pontos.append([classes.Ponto3d(float(globals.gtkBuilder.get_object('ponto1_x').get_text()),
                                               -float(globals.gtkBuilder.get_object('ponto1_y').get_text()),
                                               float(globals.gtkBuilder.get_object('ponto1_z').get_text())),
                               classes.Ponto3d(float(globals.gtkBuilder.get_object('ponto2_x').get_text()),
                                               -float(globals.gtkBuilder.get_object('ponto2_y').get_text()),
                                               float(globals.gtkBuilder.get_object('ponto2_z').get_text()))
                               ])
        globals.gtkBuilder.get_object('ponto1_x').set_text('')
        globals.gtkBuilder.get_object('ponto1_y').set_text('')
        globals.gtkBuilder.get_object('ponto1_z').set_text('')
        globals.gtkBuilder.get_object('ponto2_x').set_text('')
        globals.gtkBuilder.get_object('ponto2_y').set_text('')
        globals.gtkBuilder.get_object('ponto2_z').set_text('')

    def finalizar_forma_clicked_cb(self, btn):
        globals.pontos.append([classes.Ponto3d(float(globals.gtkBuilder.get_object('ponto1_x').get_text()),
                                               -float(globals.gtkBuilder.get_object('ponto1_y').get_text()),
                                               float(globals.gtkBuilder.get_object('ponto1_z').get_text())),
                               classes.Ponto3d(float(globals.gtkBuilder.get_object('ponto2_x').get_text()),
                                               -float(globals.gtkBuilder.get_object('ponto2_y').get_text()),
                                               float(globals.gtkBuilder.get_object('ponto2_z').get_text()))
                               ])
        lista_de_segmentos = globals.pontos.copy()
        forma3d = classes.Forma3d(globals.gtkBuilder.get_object('name_3d').get_text(), lista_de_segmentos)
        globals.shapes.append(forma3d)
        globals.gtkBuilder.get_object('list_store').append([forma3d.name, len(globals.shapes) - 1])
        globals.gtkBuilder.get_object('name_3d').set_text('')
        globals.gtkBuilder.get_object('ponto1_x').set_text('')
        globals.gtkBuilder.get_object('ponto1_y').set_text('')
        globals.gtkBuilder.get_object('ponto1_z').set_text('')
        globals.gtkBuilder.get_object('ponto2_x').set_text('')
        globals.gtkBuilder.get_object('ponto2_y').set_text('')
        globals.gtkBuilder.get_object('ponto2_z').set_text('')
        globals.gtkBuilder.get_object('dados3d_window').hide()
        globals.selected = len(globals.shapes) - 1
        transformadas.translacao3d(float(globals.gtkBuilder.get_object('drawing1').get_allocated_width() / 2) - 20,
                                   float(globals.gtkBuilder.get_object('drawing1').get_allocated_height() / 2) - 20, 0)
        globals.pontos.clear()
        viewport.redesenhar()


    def spline_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('dialogue').hide()
        globals.gtkBuilder.get_object('spline_name_window').present()

    def name_spline_ok_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('spline_name_window').hide()
        globals.gtkBuilder.get_object('dados_spline_window').present()

    def spline_mais_clicked_cb(self, btn):
        globals.pontos.append(classes.Ponto(float(globals.gtkBuilder.get_object('spline_x').get_text()),
                                            -float(globals.gtkBuilder.get_object('spline_y').get_text()),0b0000))
        globals.gtkBuilder.get_object('spline_x').set_text('')
        globals.gtkBuilder.get_object('spline_y').set_text('')

    def finalizar_spline_clicked_cb(self, btn):
        globals.pontos.append(classes.Ponto(float(globals.gtkBuilder.get_object('spline_x').get_text()),
                                            -float(globals.gtkBuilder.get_object('spline_y').get_text()),0b0000))
        lista_de_pontos = globals.pontos.copy()
        spline = classes.B_Spline(lista_de_pontos, globals.gtkBuilder.get_object('spline_name').get_text())
        globals.shapes.append(spline)
        globals.gtkBuilder.get_object('list_store').append([spline.name, len(globals.shapes) - 1])
        globals.gtkBuilder.get_object('spline_name').set_text('')
        globals.gtkBuilder.get_object('spline_x').set_text('')
        globals.gtkBuilder.get_object('spline_y').set_text('')
        globals.gtkBuilder.get_object('dados_spline_window').hide()
        viewport.ajustar_coordenadas()
        globals.pontos.clear()
        viewport.redesenhar()

    def curva_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('dialogue').hide()
        globals.gtkBuilder.get_object('curva_name_window').present()

    def name_curva_ok_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('curva_name_window').hide()
        globals.gtkBuilder.get_object('dados_curva_window').present()

    def estender_curva_clicked_cb(self, btn):
        p1 = classes.Ponto(float(globals.gtkBuilder.get_object('xp1').get_text()),
                           -float(globals.gtkBuilder.get_object('yp1').get_text()), 0b0000)
        p2 = classes.Ponto(float(globals.gtkBuilder.get_object('xp2').get_text()),
                           -float(globals.gtkBuilder.get_object('yp2').get_text()), 0b0000)
        p3 = classes.Ponto(float(globals.gtkBuilder.get_object('xp3').get_text()),
                           -float(globals.gtkBuilder.get_object('yp3').get_text()), 0b0000)
        p4 = classes.Ponto(float(globals.gtkBuilder.get_object('xp4').get_text()),
                           -float(globals.gtkBuilder.get_object('yp4').get_text()), 0b0000)
        globals.gtkBuilder.get_object('xp1').set_text('')
        globals.gtkBuilder.get_object('xp2').set_text('')
        globals.gtkBuilder.get_object('xp3').set_text('')
        globals.gtkBuilder.get_object('xp4').set_text('')
        globals.gtkBuilder.get_object('yp1').set_text('')
        globals.gtkBuilder.get_object('yp2').set_text('')
        globals.gtkBuilder.get_object('yp3').set_text('')
        globals.gtkBuilder.get_object('yp4').set_text('')
        globals.pontos.extend([p1, p2, p3, p4])


    def finalizar_curva_clicked_cb(self, btn):
        p1 = classes.Ponto(float(globals.gtkBuilder.get_object('xp1').get_text()),
                           -float(globals.gtkBuilder.get_object('yp1').get_text()), 0b0000)
        p2 = classes.Ponto(float(globals.gtkBuilder.get_object('xp2').get_text()),
                           -float(globals.gtkBuilder.get_object('yp2').get_text()), 0b0000)
        p3 = classes.Ponto(float(globals.gtkBuilder.get_object('xp3').get_text()),
                           -float(globals.gtkBuilder.get_object('yp3').get_text()), 0b0000)
        p4 = classes.Ponto(float(globals.gtkBuilder.get_object('xp4').get_text()),
                           -float(globals.gtkBuilder.get_object('yp4').get_text()), 0b0000)
        lista_de_pontos = globals.pontos.copy()
        lista_de_pontos.extend([p1, p2, p3, p4])
        curva = classes.Curva(lista_de_pontos, globals.gtkBuilder.get_object('curva_name').get_text())
        globals.shapes.append(curva)
        viewport.ajustar_coordenadas()
        globals.gtkBuilder.get_object('list_store').append([curva.name, len(globals.shapes) - 1])
        globals.gtkBuilder.get_object('xp1').set_text('')
        globals.gtkBuilder.get_object('xp2').set_text('')
        globals.gtkBuilder.get_object('xp3').set_text('')
        globals.gtkBuilder.get_object('xp4').set_text('')
        globals.gtkBuilder.get_object('yp1').set_text('')
        globals.gtkBuilder.get_object('yp2').set_text('')
        globals.gtkBuilder.get_object('yp3').set_text('')
        globals.gtkBuilder.get_object('yp4').set_text('')
        globals.gtkBuilder.get_object('dados_curva_window').hide()
        globals.pontos.clear()
        viewport.redesenhar()

    def poligono_clicked_cb(self, btn):
        globals.gtkBuilder.get_object('dialogue').hide()
        globals.name_window.present()

    def name_ok_clicked_cb(self, btn):
        globals.name_window.hide()
        globals.coordenadas_window.present()

    def mais_pontos_clicked_cb(self, btn):
        eixo_x = float(globals.gtkBuilder.get_object('coordenada_x').get_text())
        globals.gtkBuilder.get_object('coordenada_x').set_text('')
        eixo_y = -float(globals.gtkBuilder.get_object('coordenada_y').get_text())
        globals.gtkBuilder.get_object('coordenada_y').set_text('')
        ponto = classes.Ponto(eixo_x, eixo_y, 0b0000)
        globals.pontos.append(ponto)

    def finalizar_clicked_cb(self, btn):
        eixo_x = float(globals.gtkBuilder.get_object('coordenada_x').get_text())
        globals.gtkBuilder.get_object('coordenada_x').set_text('')
        eixo_y = -float(globals.gtkBuilder.get_object('coordenada_y').get_text())
        globals.gtkBuilder.get_object('coordenada_y').set_text('')
        ponto = classes.Ponto(eixo_x, eixo_y, 0b0000)
        lista_de_pontos = globals.pontos.copy()
        lista_de_pontos.append(ponto)
        globals.coordenadas_window.hide()
        poligono = classes.Polygon(globals.gtkBuilder.get_object('polygon_name').get_text(), lista_de_pontos,
                                   globals.gtkBuilder.get_object('color_button').get_rgba().red,
                                   globals.gtkBuilder.get_object('color_button').get_rgba().green,
                                   globals.gtkBuilder.get_object('color_button').get_rgba().blue)
        globals.shapes.append(poligono)
        viewport.ajustar_coordenadas()
        globals.gtkBuilder.get_object('list_store').append([poligono.name, len(globals.shapes) - 1])
        globals.pontos.clear()
        viewport.redesenhar()

    def transformar_clicked_cb(self, btn):
        if isinstance(globals.shapes[globals.selected], classes.Forma3d):
            globals.gtkBuilder.get_object('transformacoes3d').present()
        else:
            globals.trans_window.present()

    def trans3d_ok_clicked_cb(self, btn):
        transformadas.translacao3d(float(globals.gtkBuilder.get_object('trans3d_x').get_text()),
                                   -float(globals.gtkBuilder.get_object('trans3d_y').get_text()),
                                   float(globals.gtkBuilder.get_object('trans3d_z').get_text()))
        globals.gtkBuilder.get_object('trans3d_x').set_text('')
        globals.gtkBuilder.get_object('trans3d_y').set_text('')
        globals.gtkBuilder.get_object('trans3d_z').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def esc3d_ok_clicked_cb(self, btn):
        transformadas.escalonamento3d(float(globals.gtkBuilder.get_object('esc3d_x').get_text()),
                                      float(globals.gtkBuilder.get_object('esc3d_y').get_text()),
                                      float(globals.gtkBuilder.get_object('esc3d_z').get_text()))
        globals.gtkBuilder.get_object('esc3d_x').set_text('')
        globals.gtkBuilder.get_object('esc3d_y').set_text('')
        globals.gtkBuilder.get_object('esc3d_z').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def x_button_clicked_cb(self, btn):
        transformadas.rotacao3d(float(globals.gtkBuilder.get_object('graus1').get_text()), 0, 0)
        globals.gtkBuilder.get_object('graus1').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def y_button_clicked_cb(self, btn):
        transformadas.rotacao3d(float(globals.gtkBuilder.get_object('graus1').get_text()), 1, 0)
        globals.gtkBuilder.get_object('graus1').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def z_button_clicked_cb(self, btn):
        transformadas.rotacao3d(float(globals.gtkBuilder.get_object('graus1').get_text()), 2, 0)
        globals.gtkBuilder.get_object('graus1').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def outro_eixo_clicked_cb(self, btn):
        vetor = [classes.Ponto3d(float(globals.gtkBuilder.get_object('x_ponto0').get_text()),
                                 -float(globals.gtkBuilder.get_object('y_ponto0').get_text()),
                                 float(globals.gtkBuilder.get_object('z_ponto0').get_text())),
                 classes.Ponto3d(float(globals.gtkBuilder.get_object('x_ponto1').get_text()),
                                 -float(globals.gtkBuilder.get_object('y_ponto1').get_text()),
                                 float(globals.gtkBuilder.get_object('z_ponto1').get_text()))
                 ]
        transformadas.rotacao3d(float(globals.gtkBuilder.get_object('graus1').get_text()), 3, vetor)
        globals.gtkBuilder.get_object('x_ponto0').set_text('')
        globals.gtkBuilder.get_object('y_ponto0').set_text('')
        globals.gtkBuilder.get_object('z_ponto0').set_text('')
        globals.gtkBuilder.get_object('x_ponto1').set_text('')
        globals.gtkBuilder.get_object('y_ponto1').set_text('')
        globals.gtkBuilder.get_object('z_ponto1').set_text('')
        globals.gtkBuilder.get_object('transformacoes3d').hide()
        viewport.redesenhar()

    def trans_ok_clicked_cb(self, btn):
        x = float(globals.gtkBuilder.get_object('trans_x').get_text())
        y = -float(globals.gtkBuilder.get_object('trans_y').get_text())
        globals.gtkBuilder.get_object('trans_x').set_text('')
        globals.gtkBuilder.get_object('trans_y').set_text('')
        transformadas.translacao(x, y)
        globals.trans_window.hide()
        viewport.redesenhar()

    def esc_ok_clicked_cb(self, btn):
        x = float(globals.gtkBuilder.get_object('esc_x').get_text())
        y = float(globals.gtkBuilder.get_object('esc_y').get_text())
        globals.gtkBuilder.get_object('esc_x').set_text('')
        globals.gtkBuilder.get_object('esc_y').set_text('')
        transformadas.escalonamento(x, y)
        globals.trans_window.hide()
        viewport.redesenhar()

    def mundo_clicked_cb(self, btn):
        graus = float(globals.gtkBuilder.get_object('graus').get_text())
        globals.gtkBuilder.get_object('graus').set_text('')
        centro = classes.Ponto(globals.gtkBuilder.get_object('drawing1').get_allocated_width() / 2,
                               globals.gtkBuilder.get_object('drawing1').get_allocated_height() / 2,
                               0b0000)
        transformadas.rotacionar(graus, centro, 1)
        globals.trans_window.hide()
        viewport.redesenhar()

    def geometrico_clicked_cb(self, btn):
        graus = float(globals.gtkBuilder.get_object('graus').get_text())
        globals.gtkBuilder.get_object('graus').set_text('')

        transformadas.rotacionar(graus, 0, 0)
        globals.trans_window.hide()
        viewport.redesenhar()

    def arbitrario_clicked_cb(self, btn):
        graus = float(globals.gtkBuilder.get_object('graus').get_text())
        globals.gtkBuilder.get_object('graus').set_text('')
        x = float(globals.gtkBuilder.get_object('centro_x').get_text())
        y = float(globals.gtkBuilder.get_object('centro_y').get_text())
        globals.gtkBuilder.get_object('centro_x').set_text('')
        globals.gtkBuilder.get_object('centro_y').set_text('')
        centro = classes.Ponto(x, y, 0b0000)
        transformadas.rotacionar(graus, centro, 1)
        globals.trans_window.hide()
        viewport.redesenhar()

    def tree_selection_changed_cb(self, btn):
        model, iter = globals.gtkBuilder.get_object('tree_selection').get_selected()
        globals.selected = int(model[iter][1])

    def up_clicked_cb(self, btn):
        globals.camera.posicao[1] = globals.camera.posicao[1] + 50
        viewport.redesenhar()

    def down_clicked_cb(self, btn):
        globals.camera.posicao[1] = globals.camera.posicao[1] - 50
        viewport.redesenhar()

    def right_clicked_cb(self, btn):
        globals.camera.posicao[0] = globals.camera.posicao[0] - 50
        viewport.redesenhar()

    def left_clicked_cb(self, btn):
        globals.camera.posicao[0] = globals.camera.posicao[0] + 50
        viewport.redesenhar()

    def zoom_in_clicked_cb(self, btn):
        globals.camera.zoom = globals.camera.zoom * 1.1
        viewport.redesenhar()

    def zoom_out_clicked_cb(self, btn):
        globals.camera.zoom = globals.camera.zoom * 0.9
        viewport.redesenhar()

    def rotate_left_clicked_cb(self, btn):
        globals.camera.angulo = globals.camera.angulo + 0.392699082
        viewport.redesenhar()

    def rotate_right_clicked_cb(self, btn):
        globals.camera.angulo = globals.camera.angulo - 0.392699082
        viewport.redesenhar()