import pygame, time, math
from random import randint
from threading import *

pygame.init()

#inicio da tela
pygame.init()
pygame.display.set_caption("Bomber")
tela = pygame.display.set_mode((1344,704)) #, pygame.FULLSCREEN)
tela.fill((0,0,0))

imgs = []
imgs.append(pygame.image.load('Recursos/fundo.png'))
imgs.append(pygame.image.load('Recursos/qd2.png'))
imgs.append(pygame.image.load('Recursos/qd3.png'))
imgs.append(pygame.image.load('Recursos/qd4.png'))
imgs.append(pygame.image.load('Recursos/bomba.png'))#4

itens = [
    pygame.image.load('Recursos/+bomba.png'),
    pygame.image.load('Recursos/fire.png'),
    pygame.image.load('Recursos/escudo.png'),
    pygame.image.load('Recursos/chute.png'),
    pygame.image.load('Recursos/bota.png')
]

fogo = pygame.image.load('Recursos/fogo.png')

pontos_fixos = []
matriz = []
bomber = []
monstros = []
bombas = []
bomber.append([pygame.image.load('Recursos/cleo1.png'), 64, 64])
bomber.append([pygame.image.load('Recursos/cleo1.png'), 1088, 576])

#propriedade dos jogadores
velocidades = [3, 3]
qtd_bombas = [1, 1]
pode_chutar = [False, False]
tamanho_fogo = [1, 1]
escudo = [0, 0]

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

def Central_Ponto(x, y):
    global pontos_fixos, matriz
    distance = [10000, -1, -1] #valor inicial qualquer(tem q ser grande para pegar todas as distancias)
    for i in range(len(pontos_fixos)):
        for j in range(len(pontos_fixos[0])):
            if pontos_fixos[i][j][0] == 0:
                ponto1 = [matriz[i][j][0] + 32, matriz[i][j][1] + 32]
                ponto2 = [x+32, y+32]
                d = Dist(ponto1, ponto2)
                if d < distance[0]:
                    distance[0] = d
                    distance[1] = i
                    distance[2] = j
    return [distance[1],distance[2]]

def explosao(i, j, id):
    global bombas
    pt2 = [matriz[i][j][0] + 32, matriz[i][j][1] + 32]
    for b in range(len(bombas)):
        if b == id:
            continue
        pt = [bombas[b][1][0] + 32, bombas[b][1][1] + 32]
        if Dist(pt, pt2) < 64:
            return b
    return -1

def Sair_da_Bomba(b):
    sair = True
    for bb in bombas:
        ptt = [bb[1][0] + 32, bb[1][1] + 32]
        if Dist(ptt, [bomber[b][1]+32,bomber[b][2]+32]) < 64:
            sair = False
    if sair:
        return True
    else:
        return False

def Bomba_Mais_Proxima(b):
    global bombas, bomber
    try:
        tam = []
        for bb in range(len(bombas)):
            ptt = [bombas[bb][1][0] + 32, bombas[bb][1][1] + 32]
            tam.append([Dist(ptt, [bomber[b][1]+32,bomber[b][2]+32]), bb])

        menor = tam[0]
        for t in tam:
            if t[0] < menor[0]:
                menor = t

        return menor[1]
    except Exception as e:
        print(e)
        return -1

def Colisao(x, y, b): #0 = nada. 1 = bloco fixo. 2 = bloco. 3 = personagem. 4 = monstro
    global pontos_fixos, matriz, bomber, monstros, bombas
    global velocidades, qtd_bombas, pode_chutar, tamanho_fogo, escudo
    #se tiver batendo num monstro
    for m in monstros:
        pt = [m[1] + 32, m[2] + 32] #32 = metade da imagem do monstro
        if Dist(pt, [x, y]) < 64:
            return 10

    if b == 0 or b == 1:
        for bb in bombas:
            ptt = [bb[1][0] + 32, bb[1][1] + 32]
            if Dist(ptt, [x,y]) >= 64: #60 = 32 + 28
                continue
            if Dist(ptt, [x,y]) <= 20:
                continue
            if Dist([x, y], ptt) < Dist([bomber[b][1]+32, bomber[b][2]+32], ptt):
                return 11

    if b == 0:
        pt = [bomber[1][1] + 28, bomber[1][2] + 28] #28 = metade da imagem do bomber
        if Dist(pt, [x, y]) < 64:
            return 9
    elif b == 1:
        pt = [bomber[0][1] + 28, bomber[0][2] + 28] #28 = metade da imagem do bomber
        if Dist(pt, [x, y]) < 64:
            return 8
    else:
        pt = [bomber[1][1] + 28, bomber[1][2] + 28] #28 = metade da imagem do bomber
        if Dist(pt, [x, y]) < 64:
            return 9
        pt = [bomber[0][1] + 28, bomber[0][2] + 28] #28 = metade da imagem do bomber
        if Dist(pt, [x, y]) < 56:
            return 8

    pts_lados = [[x-28,y-28], [x+28,y-28], [x+28,y+28], [x-28,y+28]]
    for p in pts_lados:
        for i in range(len(pontos_fixos)):
            for j in range(len(pontos_fixos[0])):
                if pontos_fixos[i][j][0] == 1:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            return 1
                elif pontos_fixos[i][j][0] == 2:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            return 2
                elif pontos_fixos[i][j][0] > 2:
                    if matriz[i][j][0] < p[0] < (matriz[i][j][0] + 64):
                        if matriz[i][j][1] < p[1] < (matriz[i][j][1] + 64):
                            val = pontos_fixos[i][j][0]
                            #colocar os buffs nos bombers
                            if b == 0 or b == 1:
                                if pontos_fixos[i][j][0] == 3:
                                    qtd_bombas[0] += 1
                                elif pontos_fixos[i][j][0] == 4:
                                    tamanho_fogo[0] += 1
                                elif pontos_fixos[i][j][0] == 5:
                                    escudo[0] += 1
                                elif pontos_fixos[i][j][0] == 6:
                                    pode_chutar[0] = True
                                elif pontos_fixos[i][j][0] == 7:
                                    velocidades[0] += 0.5
                                pontos_fixos[i][j][0] = 0
                            return val

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
            p.append([0])
        matriz.append(m)
        pontos_fixos.append(p)

    #Colocar blocos na volta do mapa
    v = 0
    for i in range(2):
        for j in range(19):
            pontos_fixos[v][j] = [1]
        v = len(pontos_fixos) - 1

    v = 0
    for i in range(2):
        for j in range(len(pontos_fixos)):
            pontos_fixos[j][v] = [1]
        v = len(pontos_fixos[0]) - 3

    #Colocar os blocos fixos no mapa
    for i in range(2, 10, 2):
        for j in range(2, 18, 2):
            pontos_fixos[i][j] = [1]

    #Colocar o resto dos blocos no mapa
    contador = 0
    for i in range(300):
        x = randint(1,9)
        y = randint(1,17)
        tr = False
        
        if pontos_fixos[x][y][0] == 1 or pontos_fixos[x][y][0] == 2:
            tr = True

        if tr:
            i -= 1
        else:
            if contador < 10:
                pontos_fixos[x][y] = [0, randint(3, 7)]
                contador += 1
            else:
                pontos_fixos[x][y] = [0, -1]
    
    for bb in bomber:
        for i in range(len(pontos_fixos)):
            for j in range(len(pontos_fixos[0])):
                if Dist([bb[1], bb[2]], matriz[i][j]) < 100:
                    if pontos_fixos[i][j][0] == 2:
                        pontos_fixos[i][j] = [0]

def Principal(x=0):
    global velocidades, qtd_bombas, pode_chutar, tamanho_fogo, escudo
    loop = True
    Inicio_Listas()
    ok_press = [True, True]
    v_and, v_and2 = 27, 27
    #reset nas variaveis
    velocidades = [4, 3]
    qtd_bombas = [2, 1]
    pode_chutar = [True, False]
    tamanho_fogo = [3, 1]
    escudo = [0, 0]

    sair_bomba = [True, True]
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

        if sair_bomba[0] == False:
            if Sair_da_Bomba(0):
                sair_bomba[0] = True
        if sair_bomba[1] == False:
            if Sair_da_Bomba(1):
                sair_bomba[1] = True

        #-----------------------------------------personagem 1
        conseguiu = [False, False, False, False]
        X, Y = bomber[0][1], bomber[0][2]
        if key[pygame.K_w]:
            Y -= velocidades[0]
            conseguiu[2] = True
        elif key[pygame.K_s]:
            Y += velocidades[0]
            conseguiu[2] = True

        col = Colisao(X+32, Y+32, 0)
        if col == 0 and conseguiu[2]:
            conseguiu[0] = True
        else:
            if col == 11 and sair_bomba[0] and pode_chutar[0]:
                bmaisp = Bomba_Mais_Proxima(0)
                if bmaisp != -1:
                    if Y > bomber[0][2] and X == bomber[0][1]:
                        bombas[bmaisp][6] = 3
                    elif Y < bomber[0][2] and X == bomber[0][1]:
                        bombas[bmaisp][6] = 4
                    elif X > bomber[0][1] and Y == bomber[0][2]:
                        bombas[bmaisp][6] = 1
                    elif X < bomber[0][1] and Y == bomber[0][2]:
                        bombas[bmaisp][6] = 2
        if key[pygame.K_a]:
            X -= velocidades[0]
            conseguiu[3] = True
        elif key[pygame.K_d]:
            X += velocidades[0]
            conseguiu[3] = True

        col = Colisao(X+32, bomber[0][2]+32, 0)
        if col == 0 and conseguiu[3]:
            conseguiu[1] = True
        else:
            if col == 11 and sair_bomba[0] and pode_chutar[0]:
                bmaisp = Bomba_Mais_Proxima(0)
                if bmaisp != -1:
                    if Y > bomber[0][2] and X == bomber[0][1]:
                        bombas[bmaisp][6] = 3
                    elif Y < bomber[0][2] and X == bomber[0][1]:
                        bombas[bmaisp][6] = 4
                    elif X > bomber[0][1] and Y == bomber[0][2]:
                        bombas[bmaisp][6] = 1
                    elif X < bomber[0][1] and Y == bomber[0][2]:
                        bombas[bmaisp][6] = 2

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

            v_and -= velocidades[0]
            if v_and < 0:
                v_and = 27
        elif conseguiu[3]: #tentou andar
            if Colisao(X+32, Y+32+v_and, 0) == 0:
                bomber[0][2] += velocidades[0]
            elif Colisao(X+32, Y+32-v_and, 0) == 0:
                bomber[0][2] -= velocidades[0]

            v_and -= velocidades[0]
            if v_and < 0:
                v_and = 27

        #-----------------------------------------fim personagem 1
        #bombas:
        if key[pygame.K_x] and ok_press[0]:
            if qtd_bombas[0] > 0:
                pt = Central_Ponto(bomber[0][1], bomber[0][2])
                bombas.append([imgs[4], matriz[pt[0]][pt[1]], time.time(), 0, 0, [], 0])
                qtd_bombas[0] -= 1
                sair_bomba[0] = False
            ok_press[0] = False
        else:
            if not key[pygame.K_x]:
                ok_press[0] = True

        if key[pygame.K_m] and ok_press[1]:
            if qtd_bombas[1] > 0:
                pt = Central_Ponto(bomber[1][1], bomber[1][2])
                bombas.append([imgs[4], matriz[pt[0]][pt[1]], time.time(), 1, 0, [], 0])
                qtd_bombas[1] -= 1
                sair_bomba[1] = False
            ok_press[1] = False
        else:
            if not key[pygame.K_m]:
                ok_press[1] = True

        for i in range(11):
            for j in range(21):
                if pontos_fixos[i][j][0] == 0:
                    tela.blit(imgs[0], matriz[i][j])
                elif pontos_fixos[i][j][0] == 1:
                    tela.blit(imgs[1], matriz[i][j])
                elif pontos_fixos[i][j][0] == 2:
                    tela.blit(imgs[2], matriz[i][j])
                else:
                    tela.blit(itens[pontos_fixos[i][j][0]-3], matriz[i][j])

        #mostrar as bombas e fazer o processamento da explosão
        apagar = []
        for b in range(len(bombas)):
            if bombas[b][6] != 0:
                px, py = bombas[b][1][0], bombas[b][1][1]
                if bombas[b][6] == 1:
                    px += 10
                elif bombas[b][6] == 2:
                    px -= 10
                elif bombas[b][6] == 3:
                    py += 10
                elif bombas[b][6] == 4:
                    py -= 10
                if Colisao(px+32, py+32, 3) == 0:
                    bombas[b][1] = [px, py]
                else:
                    bombas[b][6] = 0
            tela.blit(bombas[b][0], (bombas[b][1][0], bombas[b][1][1]))
            if len(bombas[b][5]) > 0:
                for i in bombas[b][5]:
                    tela.blit(fogo, matriz[i[0]][i[1]])
            if (time.time() - bombas[b][2]) > 2 and bombas[b][4] == 0:
                bombas[b][6] = 0
                lc = Central_Ponto(bombas[b][1][0], bombas[b][1][1])
                bombas[b][1] = matriz[lc[0]][lc[1]]
                contador = 0
                nao_morreu = [True, True]
                a = Colisao(matriz[lc[0]][lc[1]][0] + 32, matriz[lc[0]][lc[1]][1] + 32, 3)
                c = explosao(lc[0], lc[1], b)
                if c != -1:
                    bombas[c][2] = 0
                if a == 8:
                    if escudo[0] > 0:
                        escudo[0] -= 1
                    else:
                        print("morreu")
                    nao_morreu[0] = False
                elif a == 9:
                    if escudo[1] > 0:
                        escudo[1] -= 1
                    else:
                        print("morreu")
                    nao_morreu[1] = False
                while contador <= 3:
                    for i in range(1, (tamanho_fogo[0]+1)):
                        try:
                            if contador == 0:
                                c = explosao(lc[0], lc[1]+i, b) 
                                if c != -1:
                                    bombas[c][2] = 0
                                a = Colisao(matriz[lc[0]][lc[1]+i][0] + 32, matriz[lc[0]][lc[1]+i][1] + 32, 3)
                                if a == 8 and nao_morreu[0]:
                                    if escudo[0] > 0:
                                        escudo[0] -= 1
                                    else:
                                        print("morreu")
                                    nao_morreu[0] = False
                                    break
                                elif a == 9 and nao_morreu[1]:
                                    if escudo[1] > 0:
                                        escudo[1] -= 1
                                    else:
                                        print("morreu")
                                    nao_morreu[1] = False
                                    break
                                if pontos_fixos[lc[0]][lc[1]+i][0] != 1:
                                    if pontos_fixos[lc[0]][lc[1]+i][0] == 2:
                                        if pontos_fixos[lc[0]][lc[1]+i][1] != -1:
                                            pontos_fixos[lc[0]][lc[1]+i][0] = pontos_fixos[lc[0]][lc[1]+i][1]
                                            bombas[b][5].append([lc[0],lc[1]+i])
                                            continue
                                    pontos_fixos[lc[0]][lc[1]+i] = [0]
                                    bombas[b][5].append([lc[0],lc[1]+i])
                                else:
                                    break
                            if contador == 1:
                                if (lc[1]-i) >= 0:
                                    c = explosao(lc[0], lc[1]-i, b) 
                                    if c != -1:
                                        bombas[c][2] = 0
                                    a = Colisao(matriz[lc[0]][lc[1]-i][0] + 32, matriz[lc[0]][lc[1]-i][1] + 32, 3)
                                    if a == 8 and nao_morreu[0]:
                                        if escudo[0] > 0:
                                            escudo[0] -= 1
                                        else:
                                            print("morreu")
                                        nao_morreu[0] = False
                                        break
                                    elif a == 9 and nao_morreu[1]:
                                        if escudo[1] > 0:
                                            escudo[1] -= 1
                                        else:
                                            print("morreu")
                                        nao_morreu[1] = False
                                        break
                                    if pontos_fixos[lc[0]][lc[1]-i][0] != 1:
                                        if pontos_fixos[lc[0]][lc[1]-i][0] == 2:
                                            if pontos_fixos[lc[0]][lc[1]-i][1] != -1:
                                                pontos_fixos[lc[0]][lc[1]-i][0] = pontos_fixos[lc[0]][lc[1]-i][1]
                                                bombas[b][5].append([lc[0],lc[1]-i])
                                                continue
                                        pontos_fixos[lc[0]][lc[1]-i] = [0]
                                        bombas[b][5].append([lc[0],lc[1]-i])
                                    else:
                                        break
                                        
                            if contador == 2:
                                c = explosao(lc[0]+i, lc[1], b) 
                                if c != -1:
                                    bombas[c][2] = 0
                                a = Colisao(matriz[lc[0]+i][lc[1]][0] + 32, matriz[lc[0]+i][lc[1]][1] + 32, 3)
                                if a == 8 and nao_morreu[0]:
                                    if escudo[0] > 0:
                                        escudo[0] -= 1
                                    else:
                                        print("morreu")
                                    nao_morreu[0] = False
                                    break
                                elif a == 9 and nao_morreu[1]:
                                    if escudo[1] > 0:
                                        escudo[1] -= 1
                                    else:
                                        print("morreu")
                                    nao_morreu[1] = False
                                    break
                                if pontos_fixos[lc[0]+i][lc[1]][0] != 1:
                                    if pontos_fixos[lc[0]+i][lc[1]][0] == 2:
                                        if pontos_fixos[lc[0]+i][lc[1]][1] != -1:
                                            pontos_fixos[lc[0]+i][lc[1]][0] = pontos_fixos[lc[0]+i][lc[1]][1]
                                            bombas[b][5].append([lc[0]+i,lc[1]])
                                            continue
                                    pontos_fixos[lc[0]+i][lc[1]] = [0]
                                    bombas[b][5].append([lc[0]+i,lc[1]])
                                else:
                                    break
                            if contador == 3:
                                if (lc[0]-i) >= 0:
                                    c = explosao(lc[0]-i, lc[1], b) 
                                    if c != -1:
                                        bombas[c][2] = 0
                                    a = Colisao(matriz[lc[0]-i][lc[1]][0] + 32, matriz[lc[0]-i][lc[1]][1] + 32, 3)
                                    if a == 8 and nao_morreu[0]:
                                        if escudo[0] > 0:
                                            escudo[0] -= 1
                                        else:
                                            print("morreu")
                                        nao_morreu[0] = False
                                        break
                                    elif a == 9 and nao_morreu[1]:
                                        if escudo[1] > 0:
                                            escudo[1] -= 1
                                        else:
                                            print("morreu")
                                        nao_morreu[1] = False
                                        break
                                    if pontos_fixos[lc[0]-i][lc[1]][0] != 1:
                                        if pontos_fixos[lc[0]-i][lc[1]][0] == 2:
                                            if pontos_fixos[lc[0]-i][lc[1]][1] != -1:
                                                pontos_fixos[lc[0]-i][lc[1]][0] = pontos_fixos[lc[0]-i][lc[1]][1]
                                                bombas[b][5].append([lc[0]-i,lc[1]])
                                                continue
                                        pontos_fixos[lc[0]-i][lc[1]] = [0]
                                        bombas[b][5].append([lc[0]-i,lc[1]])
                                    else:
                                        break
                        except Exception as e:
                            print(e)
                            
                    contador += 1
                bombas[b][0] = fogo
                qtd_bombas[bombas[b][3]] += 1
                bombas[b][4] = 1
                bombas[b][2] = time.time()
            elif (time.time() - bombas[b][2]) > 0.5 and bombas[b][4] == 1:
                apagar.append(b)
            
        apagar = ordenar(apagar)

        for i in apagar:
            del(bombas[i])

        for b in bomber:
            tela.blit(b[0], (b[1], b[2]-19))

        pygame.display.update()
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