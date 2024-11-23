import pygame
import numpy as np
import random

pygame.init()

RESOLUCAO = (1280, 720)

LARGURA = RESOLUCAO[0]
ALTURA = RESOLUCAO[1]

INFO_FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(LARGURA/60))

tela = pygame.display.set_mode(RESOLUCAO)
clock = pygame.time.Clock()
t = 0

pygame.display.set_caption("física-basica")

class Objeto:
    def __init__(self):
        #! Adicionar ângulo
        self.x0, self.y0 = 0, ALTURA
        self.vx, self.vy = 300, -500
        self.x, self.y = 0, 0
        self.gravidade = 200
        self.raio = 20
        self.cor = "purple"

        self.circulo = pygame.draw.circle(tela, self.cor, (self.x0, self.y0), self.raio)

    def resetar(self):
        self.x0, self.y0 = 0, ALTURA
        self.vx, self.vy = 300, -500
        self.x, self.y = 0, 0

    def atualizar(self, t):
        # Função teste. Mudar para lançamento oblíquo
        self.x = self.x0 + self.vx * t
        self.y = self.y0 + self.vy * t + 0.5 * self.gravidade * (t ** 2)

        self.circulo = pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

    #! Textos temporários, pra mostrar as velocidades. Precisa adicionar o ângulo inicial
    def mostrar_informacoes(self):
        texto_origem = f"O({self.x0},{self.y0})"
        origem = INFO_FONTE.render(texto_origem, True, "white")
        origem_retangulo = origem.get_rect(center=(0.95*LARGURA,0.40*ALTURA))
        tela.blit(origem, origem_retangulo)

        texto_vx = "vx: " + str(self.vx)
        velocidade_vx = INFO_FONTE.render(texto_vx, True, "white")
        velocidade_vx_retangulo = velocidade_vx.get_rect(center=(0.95*LARGURA,0.45*ALTURA))
        tela.blit(velocidade_vx, velocidade_vx_retangulo)

        texto_vy = "vy: " + str(self.vy)
        velocidade_vy = INFO_FONTE.render(texto_vy, True, "white")
        velocidade_vy_retangulo = velocidade_vy.get_rect(center=(0.95*LARGURA,0.5*ALTURA))
        tela.blit(velocidade_vy, velocidade_vy_retangulo)


class Alvo:
    def __init__(self):
        self.x0, self.y0 = 500, 500
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)
    
    def resetar(self):
        self.x0, self.y0 = 500, 500
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)

    def desenhar(self):
        pygame.draw.rect(tela, "green", self.rect)

    def aleatorizar_posicao(self):
        self.x0 = random.randint(0.1*LARGURA, 0.9*LARGURA)
        self.y0 = random.randint(0.1*ALTURA, 0.9*ALTURA)
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)

    # Checa se o ponto (x, y) está a uma distância do alvo
    def checar_proximidade(self, x, y):
        dist = np.sqrt((x - self.x0)**2 + (y-self.y0)**2)
        print(dist)
        if (dist < 50):
            texto = INFO_FONTE.render("Acertou!", True, "white")
            texto_retangulo = texto.get_rect(center=(0.5*LARGURA,0.9*ALTURA))
            tela.blit(texto, texto_retangulo)

            return True

        return False


objeto = Objeto()
alvo = Alvo()

#-- Lógica do loop do jogo
loop = True
pausado = False

while loop:
    dt = clock.tick(60) / 1000
    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        #! Essas mudanças so poderão acontecer antes do objeto ser "lançado"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                objeto.vy += 20
            elif event.key == pygame.K_DOWN:
                objeto.vy -= 20
            elif event.key == pygame.K_LEFT:
                objeto.vx -= 20
            elif event.key == pygame.K_RIGHT:
                objeto.vx += 20
            elif event.key == pygame.K_r:
                # Reseta para o estado inicial
                t = 0
                alvo.aleatorizar_posicao()
                objeto.resetar()
                pausado = False

    #! Por enquanto está pausado quando acerta o alvo, isso precisa mudar depois
    if (not pausado):
        tela.fill("#202020")

        objeto.atualizar(t)
        objeto.mostrar_informacoes()

        alvo.desenhar()
        if(alvo.checar_proximidade(objeto.x, objeto.y)):
            pausado = True

        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)

pygame.quit()