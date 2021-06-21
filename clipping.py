import globals
import classes


# Codifica os pontos para serem clipados por Cohen-Sutherland
def codificar(x, y):
    codigo = 0b0000

    if x > 2:
        codigo = codigo + globals.direita
    elif x < 0:
        codigo = codigo + globals.esquerda
    if y < 0:
        codigo = codigo + globals.cima
    elif y > 2:
        codigo = codigo + globals.baixo

    return codigo


# Clipagem de retas
def cohen_sutherland(ponto_a, ponto_b, option):
    if (ponto_a.code & ponto_b.code) != 0b0000:
        return None, None
    elif (ponto_a.code | ponto_b.code) != 0b0000:
        y1 = ponto_a.coordenadas[1]
        y2 = ponto_b.coordenadas[1]
        x1 = ponto_a.coordenadas[0]
        x2 = ponto_b.coordenadas[0]
        if (x2 - x1) == 0:
            m = (y2 - y1) / 0.001
        else:
            m = (y2 - y1) / (x2 - x1)
            if m == 0:
                m = 0.001

        ye = m * (0 - x1) + y1
        yd = m * (2 - x1) + y1
        xc = x1 + (0 - y1) / m
        xb = x1 + (2 - y1) / m

        if option == 1:
            if (ponto_a.code & globals.esquerda) == globals.esquerda:
                if 0 <= ye <= 2:
                    return classes.Ponto(0, ye, codificar(0, ye)), ponto_b
                else:
                    return None, None
            elif (ponto_b.code & globals.esquerda) == globals.esquerda:
                if 0 <= ye <= 2:
                    return ponto_a, classes.Ponto(0, ye, codificar(0, ye))
                else:
                    return None, None
            else:
                return ponto_a, ponto_b

        if option == 2:
            if (ponto_a.code & globals.direita) == globals.direita:
                if 0 <= yd <= 2:
                    return classes.Ponto(2, yd, codificar(2, yd)), ponto_b
                else:
                    return None, None
            elif (ponto_b.code & globals.direita) == globals.direita:
                if 0 <= yd <= 2:
                    return ponto_a, classes.Ponto(2, yd, codificar(2, yd))
                else:
                    return None, None
            else:
                return ponto_a, ponto_b

        if option == 3:
            if (ponto_a.code & globals.cima) == globals.cima:
                if 0 <= xc <= 2:
                    return classes.Ponto(xc, 0, codificar(xc, 0)), ponto_b
                else:
                    return None, None
            elif (ponto_b.code & globals.cima) == globals.cima:
                if 0 <= xc <= 2:
                    return ponto_a, classes.Ponto(xc, 0, codificar(xc, 0))
                else:
                    return None, None
            else:
                return ponto_a, ponto_b

        if option == 4:
            if (ponto_a.code & globals.baixo) == globals.baixo:
                if 0 <= xb <= 2:
                    return classes.Ponto(xb, 2, codificar(xb, 2)), ponto_b
                else:
                    return None, None
            elif (ponto_b.code & globals.baixo) == globals.baixo:
                if 0 <= xb <= 2:
                    return ponto_a, classes.Ponto(xb, 2, codificar(xb, 2))
                else:
                    return None, None
            else:
                return ponto_a, ponto_b

    else:
        return ponto_a, ponto_b


# Clipagem de poligonos
def sutherland_hodgeman():
    for formas in globals.shapes:
        if isinstance(formas, classes.Polygon):
            formas.primeira_lista.clear()
            formas.segunda_lista.clear()
            formas.terceira_lista.clear()
            formas.lista_final.clear()
            for num in range(len(formas.lista_normalizada) - 1):
                a, b = cohen_sutherland(formas.lista_normalizada[num], formas.lista_normalizada[num + 1], 1)
                if a is not None and b is not None:
                    formas.primeira_lista.append(a)
                    formas.primeira_lista.append(b)
            for num in range(len(formas.primeira_lista) - 1):
                a, b = cohen_sutherland(formas.primeira_lista[num], formas.primeira_lista[num + 1], 2)
                if a is not None and b is not None:
                    formas.segunda_lista.append(a)
                    formas.segunda_lista.append(b)
            for num in range(len(formas.segunda_lista) - 1):
                a, b = cohen_sutherland(formas.segunda_lista[num], formas.segunda_lista[num + 1], 3)
                if a is not None and b is not None:
                    formas.terceira_lista.append(a)
                    formas.terceira_lista.append(b)
            for num in range(len(formas.terceira_lista) - 1):
                a, b = cohen_sutherland(formas.terceira_lista[num], formas.terceira_lista[num + 1], 4)
                if a is not None and b is not None:
                    formas.lista_final.append(a)
                    formas.lista_final.append(b)


def sutherland_hodgeman3d():
    for formas in globals.shapes:
        if isinstance(formas, classes.Forma3d):
            formas.primeira_lista.clear()
            formas.segunda_lista.clear()
            formas.terceira_lista.clear()
            formas.lista_final.clear()
            for segmentos in formas.lista_normalizada:
                a, b = cohen_sutherland(segmentos[0], segmentos[1], 1)
                if a is not None and b is not None:
                    formas.primeira_lista.append([a, b])
            for segmentos in formas.primeira_lista:
                a, b = cohen_sutherland(segmentos[0], segmentos[1], 2)
                if a is not None and b is not None:
                    formas.segunda_lista.append([a, b])
            for segmentos in formas.segunda_lista:
                a, b = cohen_sutherland(segmentos[0], segmentos[1], 3)
                if a is not None and b is not None:
                    formas.terceira_lista.append([a, b])
            for segmentos in formas.terceira_lista:
                a, b = cohen_sutherland(segmentos[0], segmentos[1], 4)
                if a is not None and b is not None:
                    formas.lista_final.append([a, b])
