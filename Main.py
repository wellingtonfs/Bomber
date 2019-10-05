import pygame, time, math
from random import randint
from threading import *

pygame.init()

#inicio da tela
pygame.init()
#relogio = pygame.time.Clock()
pygame.display.set_caption("Bomber")
tela = pygame.display.set_mode((1344,704)) #, pygame.FULLSCREEN)
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
bomber.append([pygame.image.load('Recursos/f_bomber.png'), 64, 64]) #26 = altura dele - 64: 90 - 64
bomber.append([pygame.image.load('Recursos/f_bomber.png'), 1088, 576])

def Dist(ponto1, ponto2):
    return math.sqrt( (ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2 )

def ordenar(vetor): #ordenado de maior pra menos
    for i in range(len(vetor)):
        for j in range(i+1, len(vetor), 1):
            if vetor[j] > vetor[i]:
                aux = vetor[j]
                vetor[j] = vetor[i]
                vetor[i] = aux
    return vetor

def Colisao(x, y, b): #0 = nada. 1 = bloco fixo. 2 = bloco. 3 = personagem. 4 = monstro
    global pontos_fixos, matriz, bomber, monstros

    #se tiver batendo num monstro
    for m in monstros:
        pt = [m[1] + 32, m[2] + 32] #32 = metade da imagem do monstro
        if Dist(pt, [x, y]) < 64:
            return 4

    pts_lados = [[x-28,y-28], [x+28,y-28], [x+28,y+28], [x-28,y+28]]
    for p in pts_lados:
        for i in range(len(pontos_fixos)):
            for j in range(len(pontos_fixos[0])):
                if pontos_fixos[i][j] == 1:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            return 1
                elif pontos_fixos[i][j] == 2:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            return 2

    if b == 0:
        pt = [bomber[1][1] + 32, bomber[1][2] + 32] #32 = metade da imagem do bomber
    else:
        pt = [bomber[0][1] + 32, bomber[0][2] + 32] #32 = metade da imagem do bomber
    if Dist(pt, [x, y]) < 64:
        return 3

    return 0

def Menu():
    pass

def Inicio_Listas():
    global matriz, pontos_fixos, bomber, monstros
    matriz = []
    pontos_fixos = []

    bomber[0][1], bomber[0][2] = 64, 64
    bomber[1][1], bomber[1][2] = 1088, 576

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
    
    for bb in bomber:
        for i in range(len(pontos_fixos)):
            for j in range(len(pontos_fixos[0])):
                if Dist([bb[1], bb[2]], matriz[i][j]) < 100:
                    if pontos_fixos[i][j] == 2:
                        pontos_fixos[i][j] = 0

def Principal(x=0):
    loop = True
    Inicio_Listas()
    ok_press = [True, True]
    v_and, v_and2 = 27, 27
    #propriedade dos jogadores
    velocidades = [5, 3]
    qtd_bombas = [2, 1]
    pode_chutar = [False, False]
    tamanho_fogo = [1, 1]
    escuto = [0, 0]
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: #sair
                    loop = False
                if event.key == pygame.K_o: #resetar fase
                    return 0
                if event.key == pygame.K_p: #voltar pro menu
                    return 1
        key = pygame.key.get_pressed()

        #movimento personagem 1:
        conseguiu = [False, False, False, False]
        X, Y = bomber[0][1], bomber[0][2]
        if key[pygame.K_w]:
            Y -= velocidades[0]
            conseguiu[2] = True
        if key[pygame.K_s]:
            Y += velocidades[0]
            conseguiu[2] = True

        if Colisao(X+32, Y+32, 0) == 0 and conseguiu[2]:
            conseguiu[0] = True
        else:
            if conseguiu[2]:
                if Colisao(X+32, Y+32, 0) == 3:
                    print("morreu!")

        if key[pygame.K_a]:
            X -= velocidades[0]
            conseguiu[3] = True
        if key[pygame.K_d]:
            X += velocidades[0]
            conseguiu[3] = True

        if Colisao(X+32, bomber[0][2]+32, 0) == 0 and conseguiu[3]:
            conseguiu[1] = True
        else:
            if conseguiu[3]:
                if Colisao(X+32, bomber[0][2]+32, 0) == 3:
                    print("morreu!")

        #tratar os dados
        if conseguiu[0] and conseguiu[1]:
            bomber[0][1] = X
            bomber[0][2] = Y
            v_and = 27
        elif conseguiu[0]:
            bomber[0][2] = Y
            v_and = 27
        elif conseguiu[1]:
            bomber[0][1] = X
            v_and = 27
        elif conseguiu[2]: #tentou andar
            if Colisao(X+32+v_and, bomber[0][2], 0) == 0:
                bomber[0][1] += velocidades[0]
            elif Colisao(X+32-v_and, bomber[0][2], 0) == 0:
                bomber[0][1] -= velocidades[0]
            else:
                if Colisao(X+32+v_and, bomber[0][2], 0) == 3 or Colisao(X+32-v_and, bomber[0][2], 0) == 3:
                    print("morreu!")
            v_and -= velocidades[0]
            if v_and < 0:
                v_and = 27
        elif conseguiu[3]: #tentou andar
            if Colisao(X+32, Y+32+v_and, 0) == 0:
                bomber[0][2] += velocidades[0]
            elif Colisao(X+32, Y+32-v_and, 0) == 0:
                bomber[0][2] -= velocidades[0]
            else:
                if Colisao(X+32, Y+32+v_and, 0) == 3 or Colisao(X+32, Y+32-v_and, 0) == 3:
                    print("morreu!")
            v_and -= velocidades[0]
            if v_and < 0:
                v_and = 27

        #bombas:
        if key[pygame.K_x] and ok_press[0]:
            if qtd_bombas[0] > 0:
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

                bombas.append([matriz[distance[1]][distance[2]], time.time(), 0])
                qtd_bombas[0] -= 1
            ok_press[0] = False
        else:
            if not key[pygame.K_x]:
                ok_press[0] = True

        if key[pygame.K_m] and ok_press[1]:
            if qtd_bombas[1] > 0:
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

                bombas.append([matriz[distance[1]][distance[2]], time.time(), 1])
                qtd_bombas[1] -= 1
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

        apagar = []
        for b in range(len(bombas)):
            tela.blit(imgs[4], (bombas[b][0][0], bombas[b][0][1]))
            if (time.time() - bombas[b][1]) > 3:
                apagar.append(b)

        apagar = ordenar(apagar)

        for i in apagar:
            if bombas[i][2] == 0:
                qtd_bombas[0] += 1
            else:
                qtd_bombas[1] += 1
            del(bombas[i])

        for b in bomber:
            tela.blit(imgs[3], (b[1], b[2]))

        pygame.display.update()
        #relogio.tick(60)
    return -1

qt = True
while qt:
    Menu()
    cont = 0
    while True:
        p = Principal(cont)
        if p == -1:
            qt = False
            break
        elif p == 0:
            continue
        elif p == 1:
            cont = 0
            break
        else:
            cont += 1
            #mostra img q perdeu e quem perdeu
            #da um tempo

pygame.quit()