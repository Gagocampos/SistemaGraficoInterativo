import classes
import gi

# Arquivo contendo as variáveis globais utilizadas pelo programa

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gtkBuilder = Gtk.Builder()
gtkBuilder.add_from_file('window.glade')

shapes = []

cima = 0b1000
baixo = 0b0100
esquerda = 0b0001
direita = 0b0010

camera = classes.Camera([0, 0], 1, 0)
camera3d = classes.Camera3d()

global selected

poligonos_normalizados = []

pontos = []

name_window = gtkBuilder.get_object('polygon_name_box')

coordenadas_window = gtkBuilder.get_object('coordenada_ponto_box')

trans_window = gtkBuilder.get_object('transformacoes')

drawing_area = gtkBuilder.get_object('drawing1')

window = gtkBuilder.get_object('main_window')
window.connect('destroy', Gtk.main_quit)
