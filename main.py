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

def mostrar_texto(tam, texto, x, y):
    tamanhos = [10, 30, 60, 90]
    FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(LARGURA/tamanhos[tam]))

    t = FONTE.render(texto, True, "white")
    t_r = t.get_rect(center=(x,y))
    tela.blit(t, t_r)
    # pygame.display.update()


tela = pygame.display.set_mode(RESOLUCAO)
clock = pygame.time.Clock()
# t = 0

pygame.display.set_caption("física-basica")

class Objeto:
    def __init__(self):
        self.angulo = 0.0 # radiano
        self.tamanho_seta = 100

        self.x0, self.y0 = 200, 550
        self.vx, self.vy = 0, 0
        self.x, self.y = self.x0, self.y0
        self.arrastar = False
        self.gravidade = 200
        self.raio = 20
        self.cor = "purple"

        self.circulo = pygame.draw.circle(tela, self.cor, (self.x0, self.y0), self.raio)
        

    def desenhar_angulo(self):
        self.tamanho_seta = min(90, max(40, math.pow(self.vx**2 + self.vy**2, 0.34)))
        novo_x = self.x0 + self.tamanho_seta*np.cos(self.angulo)
        novo_y = self.y0 + self.tamanho_seta*np.sin(self.angulo)

        self.linha_angulo = pygame.draw.line(tela, self.cor, (self.x0, self.y0), (novo_x, novo_y), 5)

        # Abas da seta do ângulo
        tamanho_abas = 15
        angulo_abas = np.radians(15)

        esquerda_x = novo_x - tamanho_abas*np.cos(self.angulo + angulo_abas)
        esquerda_y = novo_y - tamanho_abas*np.sin(self.angulo + angulo_abas)

        pygame.draw.line(tela, self.cor, (novo_x, novo_y), (esquerda_x, esquerda_y), 5)

        direita_x = novo_x - tamanho_abas*np.cos(self.angulo - angulo_abas)
        direita_y = novo_y - tamanho_abas*np.sin(self.angulo - angulo_abas)

        pygame.draw.line(tela, self.cor, (novo_x, novo_y), (direita_x, direita_y), 5)

    

    def aleatorizar_posicao(self):
        self.x0 = random.randint(0.2*LARGURA, 0.8*LARGURA)
        self.y0 = random.randint(0.2*ALTURA, 0.8*ALTURA)

        self.x, self.y = self.x0, self.y0

        self.circulo = pygame.draw.circle(tela, self.cor, (self.x0, self.y0), self.raio)


    def resetar(self):
        self.__init__
    
    def voltar_origem(self):
        self.x, self.y = self.x0, self.y0

    def desenhar(self):
        self.circulo = pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

    def atualizar_posicao(self, t):
        # Função teste. Mudar para lançamento oblíquo
        self.x = self.x0 + self.vx * t
        self.y = self.y0 + self.vy * t + 0.5 * self.gravidade * (t ** 2)

        self.desenhar()

    def atualizar(self, jogo, alvo):
        if(alvo.checar_proximidade(self.x, self.y) and not jogo.acertou):
            jogo.acertou = True
            jogo.placar += 1
        
        #! Por enquanto está pausado quando acerta o alvo, isso precisa mudar depois
        if (jogo.em_movimento and not jogo.pausado):
            self.atualizar_posicao(jogo.t)

        if (not self.naTela()):
            # resetar_inicio()
            self.voltar_origem()
            # jogo.tentativas.tentativas += 1
            jogo.t = 0
            jogo.em_movimento = False

    #! Textos temporários, pra mostrar as velocidades. 
    def mostrar_informacoes(self, tempo):
        texto_origem = f"O({self.x0},{self.y0})"
        origem = INFO_FONTE.render(texto_origem, True, "white")
        origem_retangulo = origem.get_rect(center=(0.95*LARGURA,0.40*ALTURA))
        tela.blit(origem, origem_retangulo)

        angulo_graus = 0 - math.degrees(self.angulo)
        texto_angulo = "angulo: " + str(angulo_graus) + "°"
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

        tempo = INFO_FONTE.render(f"t:{tempo}", True, "white")
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
        self.aleatorizar_posicao()
        self.cor = "green"
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)
    
    def resetar(self):
        self.x0, self.y0 = 500, 500
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)

    def desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

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
            self.cor = "cyan"

            return True
        
        self.cor = "green"
        return False
    
# objeto = Objeto()
# alvo = Alvo()

#-- Lógica do loop do jogo (estados)
# loop = True
# pausado = False # Não contabiliza o tempo
# em_movimento = False # Falso quando está configurando as condições iniciais

# acertou = False # True se o objeto acertou o alvo

# Mudar essa lógica
# def resetar_inicio():
#     objeto.resetar()
#     global t
#     t = 0

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

    
# tentativas = Tentativas()        

DEBUG = False

class Jogo:
    def __init__(self):
        #-- Lógica do loop do jogo (estados)
        self.loop_jogo = True
        self.menu = True # Menu inicial
        self.pausado = False # Não contabiliza o tempo
        self.em_movimento = False # Falso quando está configurando as condições iniciais

        self.acertou = False # True se o objeto acertou o alvo
        self.mouse_apertado = False

        self.t = 0
        self.objeto = Objeto()
        self.alvo = Alvo()
        self.tentativas = Tentativas()

        self.placar = 0

    def mostrar_menu(self):
        mostrar_texto(1, "AperteSD para iniciar", 0.5*LARGURA, 0.5*ALTURA)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
                self.menu = False
                return False
            if event.type == pygame.KEYDOWN:
                self.menu = False

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.loop_jogo = False

                if not self.em_movimento:
                    if event.key == pygame.K_UP:
                        self.objeto.vy += 20
                    elif event.key == pygame.K_DOWN:
                        self.objeto.vy -= 20
                    elif event.key == pygame.K_LEFT:
                        self.objeto.vx -= 20
                    elif event.key == pygame.K_RIGHT:
                        self.objeto.vx += 20
                    elif event.key == pygame.K_a:
                        self.objeto.angulo = (self.objeto.angulo + np.radians(5))
                    elif event.key == pygame.K_d:
                        self.objeto.angulo = (self.objeto.angulo - np.radians(5))
                
                if event.key == pygame.K_r:
                    self.__init__()

                elif event.key == pygame.K_BACKSPACE:
                    # Volta objeto para origem
                    self.objeto.voltar_origem()
                    self.tentativas.tentativas = 0
                    self.t = 0
                    self.acertou = False
                    self.em_movimento = False

                elif event.key == pygame.K_p:
                    self.pausado = not self.pausado

                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    if (self.t == 0):
                        self.em_movimento = True
                        self.tentativas.tentativas += 1

            if event.type == pygame.MOUSEBUTTONDOWN and not self.em_movimento:
                self.objeto.arrastar_inicio()
                self.objeto.arrastar_fim(False)
                self.mouse_apertado = True

            if event.type == pygame.MOUSEBUTTONUP and not self.em_movimento:
                if(self.t == 0):
                    self.objeto.arrastar_fim(True)
                    self.em_movimento = True
                    self.tentativas.tentativas += 1
                self.mouse_apertado = False

        if self.mouse_apertado and not self.objeto.arrastar:
            self.objeto.arrastar_fim(False)

    def informacoes(self):
        self.objeto.desenhar()
        self.alvo.desenhar()
        self.objeto.mostrar_informacoes(self.t)
        self.tentativas.mostrar()

        if (not self.em_movimento):
            self.objeto.desenhar_angulo()

        mostrar_texto(1, f"{self.placar}", 60, 80)


    def verificar_jogada(self):
        if (self.em_movimento):
            return
        
        if (self.tentativas.tentativas >= 3 or self.acertou):
            self.alvo.aleatorizar_posicao()
            self.objeto.aleatorizar_posicao()
            self.acertou = False
            self.tentativas.tentativas = 0


    def loop(self):
        tela.fill("#202020")

        dt = clock.tick(120) / 350
        if (self.em_movimento and not self.pausado):
            self.t += dt

        while(self.menu): 
            self.mostrar_menu()
            
        self.input()
        self.informacoes()

        if (not self.em_movimento):
            mostrar_texto(1, "Configure as condições iniciais", 0.5*LARGURA,0.15*ALTURA )
            
        self.objeto.atualizar(self, self.alvo)

        self.verificar_jogada()
        
        if (self.pausado):
            mostrar_texto(1, "Pausado", 0.5*LARGURA,0.08*ALTURA)

        if (DEBUG):
            if (self.acertou):
                mostrar_texto(2, "Acertou", 0.5*LARGURA,0.5*ALTURA)

            mostrar_texto(2, f"{self.em_movimento} {self.pausado}", 0.5*LARGURA,0.3*ALTURA)

        pygame.display.update()
        pygame.display.flip()

        clock.tick(120)
        
  
jogo = Jogo()

while(jogo.loop_jogo):
    jogo.loop()

pygame.quit()
