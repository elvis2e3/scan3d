import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import arduino

puntos_base = 40
tam_pantalla = 700

verticies = [
    [-10, 0, 10],
    [10, 0, 10],
    [10, 0, -10],
    [-10, 0, -10],
    [-10, 20, 10],
    [10, 20, 10],
    [10, 20, -10],
    [-10, 20, -10],
    [3, 0, 0],
    [-3, 0, 0],
    [0, 0, 6],
    [0, 0, -4],
    ]
edges = [
    [0,1],
    [1,2],
    [2,3],
    [3,0],
    [4,5],
    [5,6],
    [6,7],
    [7,4],
    [0,4],
    [1,5],
    [2,6],
    [3,7],
    [8,9],
    [10,11],
    ]

surfaces = []
color = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (0,1,1),
    (1,0,1),
)

fondo = 0
coloreo = False

def dibujar():
    if coloreo:
        glBegin(GL_QUADS)
        for surface in surfaces:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(verticies[vertex])
                x += 1
                if x == len(color):
                    x = 0
        glEnd()
    glBegin(GL_LINES)
    for edge in edges[fondo:]:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def rotar(v, x, y, z):
    glRotatef(v, x, y, z)  # velocidad,x,y,z

def mover_objeto(x, y, z):
    glTranslatef(x, y, z)

def actualizar3d():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    dibujar()

#def main():
pygame.init()
display = (tam_pantalla, tam_pantalla)
pantalla = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
rotar_x = 0
rotar_y = 1
rotar_z = 0
rotar_v = 1
is_rotar = False
mover_objeto(0, -10, -40)
arista = 12
arista_fin = 12
puntos = 0
surf = 0
surfin = 0
fin = False

arduino = arduino.Arduino()
arduino.start()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                coloreo = not coloreo
            if event.key == pygame.K_w:
                rotar_x = 5
                rotar(5, rotar_x, 0, 0)
            if event.key == pygame.K_s:
                rotar_x = -5
                rotar(5, rotar_x, 0, 0)
            if event.key == pygame.K_a:
                rotar_y = 5
                rotar(5, 0, rotar_y, 0)
            if event.key == pygame.K_d:
                rotar_y = -5
                rotar(5, 0, rotar_y, 0)
            if event.key == pygame.K_r:
                is_rotar = not is_rotar
            if event.key == pygame.K_i:
                arduino.set_estado(1)
            if event.key == pygame.K_f:
                if fondo == 0:
                    fondo = 14
                else:
                    fondo = 0
            if event.key == pygame.K_g:
                if fin:
                    f = ((len(verticies)-12) / puntos_base) -1
                    print f
                    obj = open("scan3d.obj","w")
                    obj.write("o Scan3d\n")
                    cad = ""
                    for i in verticies[12:]:
                        cad += "v %f %f %f\n"%tuple(i)
                    cad += "usemtl Material\ns off\n"
                    j = 1
                    for i in range(1,len(verticies[12:-puntos_base])+1):
                        if j < puntos_base:
                            cad += "f %d//%d %d//%d %d//%d %d//%d\n" % (i, i + puntos_base, i + puntos_base, i + puntos_base + 1, i + puntos_base + 1, i + 1, i + 1, i)
                        else:
                            cad += "f %d//%d %d//%d %d//%d %d//%d\n" % (i, i + puntos_base, i + puntos_base, i + 1, i + 1, i - (puntos_base - 1), i - (puntos_base - 1), i)
                            j = 0
                        j +=1
                    lista = []
                    lista2 = []

                    lista.append(1)
                    lista2.append(f * puntos_base + 1)
                    for i in range(2, puntos_base + 1):
                        lista.append(i)
                        lista.append(i)
                        lista2.append(f * puntos_base + i)
                        lista2.append(f * puntos_base + i)
                    lista.append(1)
                    lista2.append(f * puntos_base + 1)
                    c = "%d//%d " * puntos_base
                    cad += ("f "+c+"\n") % tuple(lista)
                    cad += ("f "+c+"\n") % tuple(lista2)
                    obj.write(cad)
                    obj.close()
                print "el objeto se exporto con satisfaccion"
            if event.key == pygame.K_LEFT:
                mover_objeto(-0.5,0,0)
            if event.key == pygame.K_RIGHT:
                mover_objeto(0.5,0,0)
            if event.key == pygame.K_UP:
                mover_objeto(0,1,0)
            if event.key == pygame.K_DOWN:
                mover_objeto(0,-1,0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                mover_objeto(0,0,1.0)
            if event.button == 5:
                mover_objeto(0,0,-1.0)
    if is_rotar:
        rotar(rotar_v, 0, 1, 0)
    if not arduino.es_fin():
        dato = arduino.getSiguientePunto()
        if dato != None:
            verticies.append(dato)
            #print dato
            if arista > arista_fin:
                if puntos == puntos_base - 1:
                    edges.append([arista - (puntos_base - 1), arista])
                    puntos = -1
                    arista_fin += puntos_base
                edges.append([arista-1, arista])
            if arista >= 12 + puntos_base:
                edges.append([arista, arista - puntos_base])
                if surf == 1:
                    if surfin == puntos_base:
                        surfaces.append((arista-1,arista-puntos_base,arista-(puntos_base*2),(arista-1)-puntos_base))
                        surfin = 0
                        #print "***", (arista-1,arista-puntos_base,arista-(puntos_base*2),(arista-1)-puntos_base)
                    else:
                        surfaces.append((arista - 1, arista, arista - puntos_base, (arista - 1) - puntos_base))
                        #print ">>>",(arista - 1, arista, arista - puntos_base, (arista - 1) - puntos_base)
                    surf = 0
                surf += 1
                surfin += 1
            arista += 1
            puntos += 1
    else:
        if not fin:
            surfaces.append((arista - 1, arista - puntos_base, arista - (puntos_base * 2), (arista - 1) - puntos_base))
            # lista = []
            # for i in range(puntos_base):
            #     lista.append(arista-(i+1))
            # surfaces.append(lista)
            # lista = []
            # for i in range(puntos_base):
            #     lista.append(12 + i)
            # lista.append(12)
            # surfaces.append(lista)
            fin = True
    actualizar3d()
    pygame.display.flip()
    pygame.time.wait(10)
#main()
