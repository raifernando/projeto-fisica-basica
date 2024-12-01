import pygame
import numpy as np
import random
import math

pygame.init()

RESOLUCAO = (1280, 720)

LARGURA = RESOLUCAO[0]
ALTURA = RESOLUCAO[1]
tela = pygame.display.set_mode(RESOLUCAO)
clock = pygame.time.Clock()
pygame.display.set_caption("física-basica")

def mostrar_texto(tam, texto, x, y):
    tamanhos = [10, 30, 60, 90]
    FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", int(LARGURA/tamanhos[tam]))

    t = FONTE.render(texto, True, "white")
    t_r = t.get_rect(center=(x,y))
    tela.blit(t, t_r)


class Objeto:
    def __init__(self):
        self.angulo = 0.0 # radiano
        self.tamanho_seta = 100

        self.x0, self.y0 = -300, -300
        self.velocidade = 0
        self.x, self.y = self.x0, self.y0
        self.arrastar = False
        self.gravidade = 200
        self.raio = 20
        self.cor = "purple"

        self.trajetoria = []
        self.variacao_tempo_trajetoria = 0.05
        self.tempo_trajetoria = self.variacao_tempo_trajetoria

    def desenhar_angulo(self):
        self.tamanho_seta = min(90, max(40, math.pow(self.velocidade**2, 0.34)))
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
        self.y0 = random.randint(int(0.3*ALTURA), int(0.7*ALTURA))

        self.x, self.y = self.x0, self.y0


    def resetar(self):
        self.__init__
    
    def voltar_origem(self):
        self.x, self.y = self.x0, self.y0

    def desenhar(self):
        self.circulo = pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)

        # Plataforma
        pygame.draw.line(tela, self.cor, (self.x0-30, self.y0+self.raio), (self.x0+30, self.y0+self.raio), 5)

    def desenhar_trajetoria(self, t):
        if (t >= self.tempo_trajetoria):
            self.trajetoria.insert(-1, (self.x, self.y))
            self.tempo_trajetoria += self.variacao_tempo_trajetoria

        for p in self.trajetoria:
            r = pygame.Rect(p[0], p[1], 5, 5)
            pygame.draw.rect(tela, "yellow", r)


    def atualizar_posicao(self, t):
        # Função teste. Mudar para lançamento oblíquo
        vx = self.velocidade*math.cos(self.angulo)
        vy = self.velocidade*math.sin(self.angulo)

        self.x = self.x0 + vx * t
        self.y = self.y0 + vy * t + 0.5 * self.gravidade * (t ** 2)

        self.desenhar()

    def checar_colisao(self):
        esquerda, direita = self.x0-30, self.x0+30
        altura = self.y0+self.raio

        # print(esquerda, direita, altura, self.x, self.y)

        if (esquerda <= self.x <= direita and altura - 5 <= self.y <= altura + 5):
            return True
        return False
  

    #! Textos temporários, pra mostrar as velocidades. 
    def mostrar_informacoes(self, tempo):
        mostrar_texto(2, f"t:{tempo:.2f}", 0.94*LARGURA,0.35*ALTURA)

        mostrar_texto(2, f"O({self.x0},{self.y0})", 0.94*LARGURA,0.40*ALTURA)
        
        angulo_graus = 0 - math.degrees(self.angulo)
        mostrar_texto(2, f"angulo: {angulo_graus:.2f}°", 0.93*LARGURA,0.45*ALTURA)

        velocidade_convertida = self.velocidade*0.026458 #conversão de pixels por segundo para cm/s
        mostrar_texto(2, f"v: {velocidade_convertida:.2f}", 0.94*LARGURA,0.65*ALTURA)

        mostrar_texto(2, f"x:{int(self.x)} y:{int(self.y)}", 0.94*LARGURA,0.60*ALTURA)

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
        self.velocidade = min(dist*np.sqrt(3/0.5), 600) 
        


class Alvo:
    def __init__(self):
        self.x0, self.y0 = -500, -500
        self.cor = "green"
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)
    
    def resetar(self):
        self.x0, self.y0 = 500, 500
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)

    def desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

    def aleatorizar_posicao(self, objeto:Objeto):
        posicao = random.randint(1, 2)
        if (posicao == 1): #cima
            self.x0 = random.randint(0.1*LARGURA, 0.9*LARGURA)
            self.y0 = random.randint(0.1*ALTURA, int(objeto.y0*0.95))
        else:
            esquerda = random.randint(0.1*LARGURA, max(0.1*LARGURA, int(objeto.x0) - 100))
            direita = random.randint(max(0.9*LARGURA, int(objeto.x0) + 100), 0.9*LARGURA)

            self.x0 = random.choice([esquerda, direita])
            self.y0 = random.randint(int(objeto.y0*1.05), 0.9*ALTURA)
        
        self.rect = pygame.Rect(self.x0, self.y0, 50, 50)

    # Checa se o ponto (x, y) está a uma distância do alvo
    def checar_proximidade(self, x, y):
        dist = np.sqrt((x - self.x0)**2 + (y-self.y0)**2)
        # print(dist)
        if (dist < 50):
            self.cor = "cyan"
            return True
        
        self.cor = "green"
        return False
    
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

    
DEBUG = False

class Jogo:
    def __init__(self):
        # Lógica do loop do jogo (estados)
        self.loop_jogo = True
        
        self.estado_atual = {
            "menu": True,
            "configurar": False,
            "jogar": False,
            "vitoria": False,
            "derrota": False,
        }

        self.proximo_estado = self.mostrar_menu

        self.acertou = False # True se o objeto acertou o alvo
        self.mouse_apertado = False

        self.t = 0
        self.objeto = Objeto()
        self.alvo = Alvo()
        self.tentativas = Tentativas()

        self.placar = 0

    #--- Funções auxiliares
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.loop_jogo = False
                elif event.key == pygame.K_r:
                    self.__init__()
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    if (self.t == 0):
                        return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.objeto.arrastar_inicio()
                self.objeto.arrastar_fim(False)
                self.mouse_apertado = True

            if event.type == pygame.MOUSEBUTTONUP:
                if(self.t == 0):
                    self.objeto.arrastar_fim(True)
                self.mouse_apertado = False
                return True

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.objeto.velocidade = min(600, max(0, self.objeto.velocidade+3))
        if keys[pygame.K_DOWN]:
            self.objeto.velocidade = min(600, max(0, self.objeto.velocidade-3))
        if keys[pygame.K_LEFT]:
            self.objeto.angulo -= np.radians(1)
        if keys[pygame.K_RIGHT]:
            self.objeto.angulo += np.radians(1)

        if self.mouse_apertado and not self.objeto.arrastar:
            self.objeto.arrastar_fim(False)
    
        return False

    def informacoes(self):
        self.alvo.desenhar()
        self.objeto.desenhar()
        self.objeto.mostrar_informacoes(self.t)
        self.tentativas.mostrar()

        if self.acertou:
            mostrar_texto(2, "Acertou!", 0.5*LARGURA,0.9*ALTURA )

        mostrar_texto(1, f"{self.placar}", 60, 80)

    def resetar_tentativa(self):
        self.t = 0
        self.objeto.trajetoria = []
        self.objeto.tempo_trajetoria = 0
        self.acertou = False
        self.objeto.voltar_origem()

    #--- Estados do jogo
    def mostrar_menu(self):
        if not self.estado_atual["menu"]:
            self.proximo_estado = self.resetar
        
        mostrar_texto(1, "Aperte para iniciar", 0.5*LARGURA, 0.5*ALTURA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
                self.estado_atual["menu"] = False
            if event.type == pygame.KEYDOWN:
                self.estado_atual["menu"] = False

    def resetar(self):
        self.objeto.aleatorizar_posicao()
        self.alvo.aleatorizar_posicao(self.objeto)

        self.tentativas.tentativas = 0

        self.estado_atual["configurar"] = True
        self.proximo_estado = self.configurar


    def configurar(self):
        self.informacoes()
        mostrar_texto(1, "Configure as condições iniciais", 0.5*LARGURA,0.15*ALTURA)
        self.objeto.desenhar_angulo()

        self.resetar_tentativa()

        self.estado_atual["configurar"] = not self.input()
        if not self.estado_atual["configurar"]:
            self.proximo_estado = self.jogar
            self.estado_atual["jogar"] =  True
            self.tentativas.tentativas += 1

    def jogar(self):    
        dt = clock.tick(120) / 350
        self.t += dt

        if self.alvo.checar_proximidade(self.objeto.x, self.objeto.y):
            self.acertou = True

        self.objeto.desenhar_trajetoria(self.t)
        self.objeto.atualizar_posicao(self.t)

        if not self.objeto.naTela() or self.objeto.checar_colisao():
            self.estado_atual["jogar"] = False
            if self.acertou:
                self.estado_atual["vitoria"] = True
                self.proximo_estado = self.vitoria
            elif self.tentativas.tentativas >= 3:
                self.estado_atual["derrota"] = True
                self.proximo_estado = self.derrota
            else:
                self.estado_atual["configurar"] = True
                self.proximo_estado = self.configurar

    def vitoria(self):
        self.placar += 1
        self.estado_atual["vitoria"] = False
        self.proximo_estado = self.resetar

    def derrota(self):
        self.placar = 0
        self.estado_atual["derrota"] = False
        self.proximo_estado = self.resetar

    def executar_proximo_estado(self):
        self.proximo_estado()

    #--- Loop do jogo
    def loop(self):
        tela.fill("#202020")
        
        self.proximo_estado()

        if (not self.estado_atual["menu"] and not self.estado_atual["configurar"]):
            self.informacoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.loop_jogo = False

        pygame.display.update()
        pygame.display.flip()

        clock.tick(120)
  

jogo = Jogo()

while(jogo.loop_jogo):
    jogo.loop()

pygame.quit()
