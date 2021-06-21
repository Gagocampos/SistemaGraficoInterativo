import globals
import classes


# Definição do scrip para interpretar arquivos .obj
def read_object(nome):
    vertices_normalizados = []
    faces = []
    name = []
    linhas = []
    with open(nome, 'r') as file:
        for line in file:
            if line[0] == 'v':
                vertices_normalizados.append(line.rstrip("\n").split(' '))
            elif line[0] == 'f':
                if line.find('/') == -1:
                    faces.append(line.rstrip("\n").split(' '))
            elif line[0] == 'l':
                linhas.append(line.rstrip("\n").split(' '))
            elif line[0] == 'g' or line[0] == 'o':
                name.append(line.rstrip("\n").split(' '))

    vertices = []
    for vertice in vertices_normalizados:
        vertices.append([(float(vertice[1]) + 1)*float(globals.gtkBuilder.get_object('drawing1').get_allocated_width()-40)/2,
                         (-float(vertice[2]) + 1)*float(globals.gtkBuilder.get_object('drawing1').get_allocated_height()-40)/2,
                         float(vertice[3]) * 20])

    superficie = []
    for linha in linhas:
        for n in range(len(linha) - 1):
            superficie.append(classes.Ponto3d(vertices[int(linha[n+1]) - 1][0],
                                              vertices[int(linha[n+1]) - 1][1], vertices[int(linha[n+1]) - 1][2]))

    forma3d = []
    for face in faces:
        for pontos in range(len(face) - 2):
            forma3d.append([classes.Ponto3d(vertices[int(face[pontos + 1]) - 1][0] ,
                                            vertices[int(face[pontos + 1]) - 1][1],
                                            vertices[int(face[pontos + 1]) - 1][2]),
                            classes.Ponto3d(vertices[int(face[pontos + 2]) - 1][0],
                                            vertices[int(face[pontos + 2]) - 1][1],
                                            vertices[int(face[pontos + 2]) - 1][2])
                            ])
    if name:
        if forma3d:
            globals.shapes.append(classes.Forma3d(name[0][1], forma3d))
        elif superficie:
            globals.shapes.append(classes.Superficie(superficie, name[0][1]))
        globals.gtkBuilder.get_object('list_store').append([name[0][1], len(globals.shapes) - 1])
    else:
        if forma3d:
            globals.shapes.append(classes.Forma3d('Sem nome', forma3d))
        elif superficie:
            globals.shapes.append(classes.Superficie(superficie, 'Sem nome'))
        globals.gtkBuilder.get_object('list_store').append(['Sem nome', len(globals.shapes) - 1])