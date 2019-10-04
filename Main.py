import pygame, time, math
from random import randint
from threading import *

pygame.init()

#inicio da tela
pygame.init()
#relogio = pygame.time.Clock()
pygame.display.set_caption("Bomber")
tela = pygame.display.set_mode((1344,704)) #720), pygame.FULLSCREEN)
tela.fill((0,0,0))

imgs = []
imgs.append(pygame.image.load('Recursos/qd1.png'))
imgs.append(pygame.image.load('Recursos/qd2.png'))
imgs.append(pygame.image.load('Recursos/qd3.png'))
imgs.append(pygame.image.load('Recursos/qd4.png'))
imgs.append(pygame.image.load('Recursos/bomba.png'))#4

pontos_fixos = []
matriz = []
bomber = []
monstros = []
bombas = []
bomber.append([pygame.image.load('Recursos/f_bomber.png'), 64, 64-26]) #26 = altura dele - 64: 90 - 64
bomber.append([pygame.image.load('Recursos/f_bomber.png'), 1088, 576-26])

def Dist(ponto1, ponto2):
    return math.sqrt( (ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2 )

def Colisao(x, y):
    global pontos_fixos, matriz
    pts_lados = [[x-28,y-28], [x+32,y-28], [x+32,y+28], [x-32,y+28]]
    for p in pts_lados:
        for i in range(len(pontos_fixos)):
            for j in range(len(pontos_fixos[0])):
                if pontos_fixos[i][j] != 0:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            return True
    return False

def Menu():
    pass

def Inicio_Listas():
    global matriz, pontos_fixos
    matriz = []
    pontos_fixos = []
    for i in range(11):
        m = []
        p = []
        for j in range(21):
            m.append([j*64, i*64])
            p.append(0)
        matriz.append(m)
        pontos_fixos.append(p)

    #Colocar blocos na volta do mapa
    v = 0
    for i in range(2):
        for j in range(19):
            pontos_fixos[v][j] = 1
        v = len(pontos_fixos) - 1

    v = 0
    for i in range(2):
        for j in range(len(pontos_fixos)):
            pontos_fixos[j][v] = 1
        v = len(pontos_fixos[0]) - 3

    #Colocar os blocos fixos no mapa
    for i in range(2, 10, 2):
        for j in range(2, 18, 2):
            pontos_fixos[i][j] = 1

    #Colocar o resto dos blocos no mapa
    for i in range(300):
        x = randint(1,9)
        y = randint(1,17)
        tr = False
        
        if pontos_fixos[x][y] == 1 or pontos_fixos[x][y] == 2:
            tr = True

        if tr:
            i -= 1
        else:
            pontos_fixos[x][y] = 0

def Principal():
    loop = True
    Inicio_Listas()
    ok_press = [True, True]
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loop = False

        key = pygame.key.get_pressed()

        #movimento personagem 1:
        conseguiu = [False, False]
        X, Y = bomber[0][1], bomber[0][2]
        if key[pygame.K_w]:
            Y -= 1
        if key[pygame.K_s]:
            Y += 1
        if not Colisao(X+32, Y+32):
            conseguiu[0] = True
        if key[pygame.K_a]:
            X -= 1
        if key[pygame.K_d]:
            X += 1
        if not Colisao(X+32, bomber[0][2]+32):
            conseguiu[1] = True

        if conseguiu[0]:
            bomber[0][2] = Y
        if conseguiu[1]:
            bomber[0][1] = X

        conseguiu = [False, False]
        X, Y = bomber[1][1], bomber[1][2]
        #movimento personagem 2:
        if key[pygame.K_UP]:
            Y -= 3
        if key[pygame.K_DOWN]:
            Y += 3
        if not Colisao(X+32, Y+32):
            conseguiu[0] = True
        if key[pygame.K_LEFT]:
            X -= 3
        if key[pygame.K_RIGHT]:
            X += 3
        if not Colisao(X+32, bomber[1][2]+32):
            conseguiu[1] = True
        
        if conseguiu[0]:
            bomber[1][2] = Y
        if conseguiu[1]:
            bomber[1][1] = X

        #bombas:
        if key[pygame.K_x] and ok_press[0]:
            distance = [10000, -1, -1] #valor inicial qualquer(tem q ser grande para pegar todas as distancias)
            for i in range(len(pontos_fixos)):
                for j in range(len(pontos_fixos[0])):
                    if pontos_fixos[i][j] == 0:
                        ponto1 = [matriz[i][j][0] + 32, matriz[i][j][1] + 32]
                        ponto2 = [bomber[0][1]+32, bomber[0][2]+30]
                        d = Dist(ponto1, ponto2)
                        if d < distance[0]:
                            distance[0] = d
                            distance[1] = i
                            distance[2] = j

            bombas.append(matriz[distance[1]][distance[2]])
            ok_press[0] = False
        else:
            if not key[pygame.K_x]:
                ok_press[0] = True

        if key[pygame.K_m] and ok_press[1]:
            distance = [10000, -1, -1] #valor inicial qualquer(tem q ser grande para pegar todas as distancias)
            for i in range(len(pontos_fixos)):
                for j in range(len(pontos_fixos[0])):
                    if pontos_fixos[i][j] == 0:
                        ponto1 = [matriz[i][j][0] + 32, matriz[i][j][1] + 32]
                        ponto2 = [bomber[1][1]+32, bomber[1][2]+30] #32 e 30 é para a bomba ser colocada em relação ao pé do jogador
                        d = Dist(ponto1, ponto2)
                        if d < distance[0]:
                            distance[0] = d
                            distance[1] = i
                            distance[2] = j

            bombas.append(matriz[distance[1]][distance[2]])
            ok_press[1] = False
        else:
            if not key[pygame.K_m]:
                ok_press[1] = True

        for i in range(11):
            for j in range(21):
                if pontos_fixos[i][j] == 0:
                    tela.blit(imgs[0], matriz[i][j])
                elif pontos_fixos[i][j] == 1:
                    tela.blit(imgs[1], matriz[i][j])
                elif pontos_fixos[i][j] == 2:
                    tela.blit(imgs[2], matriz[i][j])

        for bomba in bombas:
            tela.blit(imgs[4], (bomba[0], bomba[1]))

        for b in bomber:
            tela.blit(imgs[3], (b[1], b[2]))

        pygame.display.update()
        #relogio.tick(60)

Principal()

pygame.quit()