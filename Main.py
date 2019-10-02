import pygame, time
from random import randint
from threading import *

pygame.init()

#inicio da tela
pygame.init()
relogio = pygame.time.Clock()
pygame.display.set_caption("Bomber")
tela = pygame.display.set_mode((1344,704)) #720), pygame.FULLSCREEN)
tela.fill((0,0,0))

imgs = []
imgs.append(pygame.image.load('Recursos/qd1.png'))
imgs.append(pygame.image.load('Recursos/qd2.png'))
imgs.append(pygame.image.load('Recursos/qd3.png'))
imgs.append(pygame.image.load('Recursos/qd4.png'))

pontos_fixos = []
matriz = []
bomber = []
bomber.append(pygame.image.load('Recursos/f_bomber.png'))

#criar matriz de pontos:
for i in range(11):
    m = []
    for j in range(21):
        m.append([j*64, i*64])
    matriz.append(m)

for i in range(1, 20, 2):
    for j in range(1, 10, 2):
        pontos_fixos.append([j, i])

def Principal():
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loop = False

        ant = 0
        for i in range(11):
            if ant == 0:
                m = 1
            else:
                m = 0
            ant = m
            for j in range(21):
                tela.blit(imgs[m], (j*64,i*64))
                if m == 0:
                    m = 1
                else:
                    m = 0

        pontos = []
        for i in range(100):
            x = randint(0,10)
            y = randint(0,20)
            tr = False
            for j in pontos:
                if j[0] == x and j[1] == y:
                    tr = True
            
            for j in pontos_fixos:
                if j[0] == x and j[1] == y:
                    tr = True

            if tr:
                i -= 1
            else:
                pontos.append([x, y])

        print(pontos_fixos)
        for i in pontos_fixos:
            tela.blit(imgs[3], matriz[i[0]][i[1]])

        for i in pontos:
            tela.blit(imgs[2], matriz[i[0]][i[1]])

        pygame.display.update()
        relogio.tick(60)
        time.sleep(2)

Principal()

pygame.quit()