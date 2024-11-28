import pygame
import numpy as np
import random
import math
from sympy import Line

pygame.init()

RESOLUCAO = (1280, 720)

LARGURA = RESOLUCAO[0]
ALTURA = RESOLUCAO[1]

INFO_FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(LARGURA/60))
PEQUENA_FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(LARGURA/30))

tela = pygame.display.set_mode(RESOLUCAO)
clock = pygame.time.Clock()
t = 0

pygame.display.set_caption("física-basica")

class Objeto:
    def __init__(self):
        self.angulo = 0
        self.x0, self.y0 = 200, 550
        self.vx, self.vy = 0, 0
        self.x, self.y = self.x0, self.y0
        self.arrastar = False
        self.gravidade = 200
        self.raio = 20
        self.cor = "purple"

        self.circulo = pygame.draw.circle(tela, self.cor, (self.x0, self.y0), self.raio)

    def resetar(self):
        self.__init__
    
    def voltar_origem(self):
        self.x, self.y = self.x0, self.y0

    def desenhar(self):
        self.circulo = pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

    def atualizar(self, t):
        # Função teste. Mudar para lançamento oblíquo
        self.x = self.x0 + self.vx * t
        self.y = self.y0 + self.vy * t + 0.5 * self.gravidade * (t ** 2)

        self.desenhar()

    #! Textos temporários, pra mostrar as velocidades. 
    def mostrar_informacoes(self, tempo):
        texto_origem = f"O({self.x0},{self.y0})"
        origem = INFO_FONTE.render(texto_origem, True, "white")
        origem_retangulo = origem.get_rect(center=(0.95*LARGURA,0.40*ALTURA))
        tela.blit(origem, origem_retangulo)

        angulo_graus = 0 - math.degrees(self.angulo)
        texto_angulo = "angulo: " + str(angulo_graus)
        angulo = INFO_FONTE.render(texto_angulo, True, "white")
        angulo_retangulo = angulo.get_rect(center=(0.95*LARGURA,0.45*ALTURA))
        tela.blit(angulo, angulo_retangulo)


        texto_vx = "vx: " + str(self.vx)
        velocidade_vx = INFO_FONTE.render(texto_vx, True, "white")
        velocidade_vx_retangulo = velocidade_vx.get_rect(center=(0.95*LARGURA,0.50*ALTURA))
        tela.blit(velocidade_vx, velocidade_vx_retangulo)

        texto_vy = "vy: " + str(self.vy)
        velocidade_vy = INFO_FONTE.render(texto_vy, True, "white")
        velocidade_vy_retangulo = velocidade_vy.get_rect(center=(0.95*LARGURA,0.55*ALTURA))
        tela.blit(velocidade_vy, velocidade_vy_retangulo)

        texto_pos = f"x:{self.x} y:{self.y}"
        pos = INFO_FONTE.render(texto_pos, True, "white")
        pos_retangulo = pos.get_rect(center=(0.95*LARGURA,0.60*ALTURA))
        tela.blit(pos, pos_retangulo)

        tempo = INFO_FONTE.render(f"t:{t}", True, "white")
        tempo_retangulo = tempo.get_rect(center=(0.95*LARGURA,0.35*ALTURA))
        tela.blit(tempo, tempo_retangulo)

    def naTela(self):
        if (int(self.x) >= 0 and int(self.x) <= LARGURA and int(self.y) >= 0 and int(self.y) <= ALTURA):
            return True
        return False


    def arrastar_inicio(self):
       self.arrastar = True

    def arrastar_fim(self, encerrar=False):
        self.arrastar = encerrar
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos

        dx = self.x - mouse_x
        dy = self.y - mouse_y
        
        self.angulo = math.atan2(dy, dx)  
        dist = math.hypot(dx, dy)

        #formula obtida da conservacao de energia: o valor de cima é a constantes elastica, o de baixo a massa
        velocidade = dist*np.sqrt(3/0.5) 
        self.vx = velocidade*math.cos(self.angulo)
        self.vy = velocidade*math.sin(self.angulo)


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

#-- Lógica do loop do jogo (estados)
loop = True
pausado = False # Não contabiliza o tempo
em_movimento = False # Falso quando está configurando as condições iniciais

acertou = False # True se o objeto acertou o alvo

# Mudar essa lógica
def resetar_inicio():
    objeto.resetar()
    global t
    t = 0

class Tentativas:
    def __init__(self):
        self.tentativas = 0
        self.raio = 10
        self.borda = 1
        self.origem = (30, 30)

    def mostrar(self):
        for i in range(0, 3):
            preencher = 0 if i < self.tentativas else self.borda
            pygame.draw.circle(tela, "white", (self.origem[0]*(i+1), self.origem[1]), radius=self.raio, width=preencher)

    
tentativas = Tentativas()        

mouse_apertado = False

while loop:
    dt = clock.tick(120) / 350
    if (em_movimento and not pausado):
        t += dt

    tela.fill("#202020")

    tentativas.mostrar()

    if (not em_movimento):
        texto = PEQUENA_FONTE.render(f"Configure as condições iniciais", True, "white")
        texto_retangulo = texto.get_rect(center=(0.5*LARGURA,0.15*ALTURA))
        tela.blit(texto, texto_retangulo)

    if (acertou):
        texto = PEQUENA_FONTE.render("Acertou", True, "white")
        texto_retangulo = texto.get_rect(center=(0.5*LARGURA,0.5*ALTURA))
        tela.blit(texto, texto_retangulo)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            loop = False
        #! Essas mudanças so poderão acontecer antes do objeto ser "lançado"
        if event.type == pygame.KEYDOWN:
            if not em_movimento:
                if event.key == pygame.K_UP:
                    objeto.vy += 20
                elif event.key == pygame.K_DOWN:
                    objeto.vy -= 20
                elif event.key == pygame.K_LEFT:
                    objeto.vx -= 20
                elif event.key == pygame.K_RIGHT:
                    objeto.vx += 20
            
            if event.key == pygame.K_r:
                # Reseta o jogo
                resetar_inicio()
                acertou = False
                em_movimento = False
                alvo.aleatorizar_posicao()

            elif event.key == pygame.K_BACKSPACE:
                # Volta objeto para origem
                objeto.voltar_origem()
                tentativas.tentativas = 0
                t = 0
                acertou = False
                em_movimento = False

            elif event.key == pygame.K_p:
                pausado = not pausado

            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                if (t == 0):
                    em_movimento = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            objeto.arrastar_inicio()
            objeto.arrastar_fim(False)
            mouse_apertado = True


        if event.type == pygame.MOUSEBUTTONUP:
            if(t == 0):
                objeto.arrastar_fim(True)
                em_movimento = True
            mouse_apertado = False

    if mouse_apertado and not objeto.arrastar:
        objeto.arrastar_fim(False)


    objeto.desenhar()
    alvo.desenhar()
    objeto.mostrar_informacoes(t)

    texto = PEQUENA_FONTE.render(f"{em_movimento} {pausado}", True, "white")
    texto_retangulo = texto.get_rect(center=(0.5*LARGURA,0.3*ALTURA))
    tela.blit(texto, texto_retangulo)

    if(alvo.checar_proximidade(objeto.x, objeto.y)):
        acertou = True
    
    #! Por enquanto está pausado quando acerta o alvo, isso precisa mudar depois
    if (em_movimento and not pausado):
        objeto.atualizar(t)

    if (not objeto.naTela()):
        # resetar_inicio()
        objeto.voltar_origem()
        tentativas.tentativas += 1
        t = 0
        em_movimento = False

    # em_movimento = objeto.naTela()

    if (pausado):
        texto = PEQUENA_FONTE.render("Aperte [enter] para continuar.", True, "white")
        texto_retangulo = texto.get_rect(center=(0.5*LARGURA,0.1*ALTURA))
        tela.blit(texto, texto_retangulo)

    pygame.display.update()
    pygame.display.flip()

    clock.tick(120)


pygame.quit()
