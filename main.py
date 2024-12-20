"""
Nome do Projeto: Acerto ao Alvo. 

Descrição: Um jogo cujo objetivo principal é que um alvo colocado em posição aleatória seja atingido por uma bola. Para que isso aconteça, o jogador deve controlar o vetor velocidade (módulo, direção e sentido) do objeto lançado.
A modelagem física do jogo simula um lançamento oblíquo, estando todos os corpos móveis sujeitos à ação de um campo gravitacional constante e, portanto, percorrendo uma trajetória parabólica, que é desenhada na tela.

Autores: 
  Raí Fernando Dal Prá - 15506968
  Lucas Dúckur Nunes Andreolli - 15471518
  Yan Trindade Meireles - 13680035
  Rafael Perez Carmanhani - 15485420
  
Este projeto faz parte do processo avaliativo da disciplina 7600105 - Física Básica I (2024) da USP-São Carlos ministrada pela Prof. Krissia de Zawadzki.
"""

# Importação de bibliotecas necessárias
import pygame
import numpy as np
import random
import math
import os

pygame.init()


# --- Configurações iniciais do jogo ---
RESOLUCAO = (1280, 720) # Dimensão da janela do jogo.


LARGURA = RESOLUCAO[0]
ALTURA = RESOLUCAO[1]
tela = pygame.display.set_mode(RESOLUCAO) # Inicializa a tela.
clock = pygame.time.Clock() # Configura o controle de FPS.
pygame.display.set_caption("Projeto Final Física Básica")

def mostrar_texto(tam, texto, x, y, customizado=0, cor="white"):
    """
    Renderiza texto na tela em uma posição e tamanho específicos.
    """
    tamanhos = [10, 30, 60, 75]
    tamanho_fonte = int(LARGURA/tamanhos[tam])
    if customizado:
        tamanho_fonte = int(LARGURA/customizado)

    FONTE = pygame.font.Font("assets/font/GetVoIP-Grotesque.ttf", tamanho_fonte)

    t = FONTE.render(texto, True, cor)
    t_r = t.get_rect(center=(x,y))
    tela.blit(t, t_r)


class Objeto:
    """
    Representa o objeto lançado pelo jogador (bola).
    Modelagem física baseada em lançamento oblíquo:
    - Velocidade inicial (vetorial): composta por ângulo e módulo.
    - Aceleração gravitacional constante.
    - Movimento descrito por funções quadráticas para a posição.
    """
  
    def __init__(self):
        self.angulo = 0.0 # Ângulo do lançamento (em radianos).
        self.tamanho_seta = 100 # Tamanho do vetor que indica a direção do lançamento.

        self.x0, self.y0 = -300, -300 # Posição inicial do objeto.
        self.velocidade = 0
        self.velocidade_maxima = 945
        self.x, self.y = self.x0, self.y0 # Posição atual do objeto.
        self.arrastar = False
        self.gravidade = 370 # Aceleração gravitacional.
        self.cor = pygame.Color("#ab6202")

        self.trajetoria = []
        self.variacao_tempo_trajetoria = 0.05
        self.tempo_trajetoria = self.variacao_tempo_trajetoria

        self.imagem_rock = pygame.image.load("assets/img/rock.png")  # Caminho da imagem
        self.imagem_rock = pygame.transform.scale(self.imagem_rock, (50, 50))  # Redimensionar (ajustar conforme necessário)
        self.raio = self.imagem_rock.get_width() // 2
        self.largura_imagem = self.imagem_rock.get_width()
        self.altura_imagem = self.imagem_rock.get_height()

    def desenhar_angulo(self):
        """
        Desenha o vetor representando a direção e força do lançamento.
        """
      
        self.tamanho_seta = min(90, max(40, math.pow(self.velocidade**2, 0.34)))
        novo_x = self.x0 + self.tamanho_seta*np.cos(self.angulo)
        novo_y = self.y0 + self.tamanho_seta*np.sin(self.angulo)

        # Desenha a linha principal do vetor.
        self.linha_angulo = pygame.draw.line(tela, self.cor, (self.x0, self.y0), (novo_x, novo_y), 5)

        # Desenha as abas da seta (indicador de sentido).
        tamanho_abas = 15
        angulo_abas = np.radians(15)

        esquerda_x = novo_x - tamanho_abas*np.cos(self.angulo + angulo_abas)
        esquerda_y = novo_y - tamanho_abas*np.sin(self.angulo + angulo_abas)

        pygame.draw.line(tela, self.cor, (novo_x, novo_y), (esquerda_x, esquerda_y), 5)

        direita_x = novo_x - tamanho_abas*np.cos(self.angulo - angulo_abas)
        direita_y = novo_y - tamanho_abas*np.sin(self.angulo - angulo_abas)

        pygame.draw.line(tela, self.cor, (novo_x, novo_y), (direita_x, direita_y), 5)

    def aleatorizar_posicao(self, nivel):
        """
        Define a posição inicial do objeto com base no nível atual.
        """
      
        posicao_x = posicao_y = 0
        nivel = (nivel % 5) + 1 
        
        match nivel:
            case 0 | 1 | 2:
                posicao_x = random.uniform(0.4, 0.6)*LARGURA 
                posicao_y = random.uniform(0.6, 0.5)*ALTURA
            case 3:
                posicao_x = random.uniform(0.4, 0.6)*LARGURA 
                posicao_y = random.uniform(0.7, 0.55)*ALTURA
            case 4:
                posicao_x = random.choice([random.uniform(0.2, 0.3), random.uniform(0.7, 0.8)])*LARGURA
                posicao_y = random.uniform(0.6, 0.7)*ALTURA
            case 5:
                posicao_x = 0.5*LARGURA
                posicao_y = 0.4*ALTURA
            case _:
                posicao_x = random.randint(0.1*LARGURA, 0.9*LARGURA)
                posicao_y = random.randint(0.1*ALTURA, 0.9*ALTURA)
        
        self.x0, self.y0 = posicao_x, posicao_y


    def resetar(self):
        self.__init__
    
    def voltar_origem(self):
        self.x, self.y = self.x0, self.y0

    def desenhar(self):
        tela.blit(self.imagem_rock, (self.x - self.imagem_rock.get_width() // 2, self.y - self.imagem_rock.get_height() // 2))
        pygame.draw.line(tela, self.cor, (self.x0-30, self.y0+self.raio), (self.x0+30, self.y0+self.raio), 5)


    def desenhar_trajetoria(self, t):
        if (t >= self.tempo_trajetoria):
            self.trajetoria.insert(-1, (self.x, self.y))
            self.tempo_trajetoria += self.variacao_tempo_trajetoria

        for p in self.trajetoria:
            r = pygame.Rect(p[0], p[1], 5, 5)
            pygame.draw.rect(tela, "yellow", r)


    def atualizar_posicao(self, t):
        vx = self.velocidade*math.cos(self.angulo)
        vy = self.velocidade*math.sin(self.angulo)

        self.x = self.x0 + vx * t
        self.y = self.y0 + vy * t + 0.5 * self.gravidade * (t ** 2)

        self.desenhar()

    def checar_colisao(self):
        """
        Verifica se o objeto colidiu com o chão (linha de plataforma).
        """
      
        esquerda, direita = self.x0-30, self.x0+30
        altura = self.y0+self.raio

        if (esquerda <= self.x <= direita and altura - 5 <= self.y <= altura + 5):
            return True
        return False
  

    def mostrar_informacoes(self, tempo):
        angulo_graus = (0 - math.degrees(self.angulo)) % 360
        
        velocidade_convertida = self.velocidade*0.026458 #conversão de pixels por segundo para cm/s
        
        angulo = f"ângulo: {angulo_graus:.2f}°"
        velocidade = f"velocidadade: {velocidade_convertida:.2f} m/s"

        mostrar_texto(3, angulo + " | " + velocidade, 0.5*LARGURA,0.95*ALTURA)

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
        self.velocidade = min(dist*np.sqrt(3/0.5), self.velocidade_maxima) 
        

# --- Classe Alvo ---
class Alvo:
    """
    Representa o alvo que o jogador deve atingir.
    """
  
    def __init__(self):
        self.x0, self.y0 = -500, -500
        self.largura = 100
        self.cor = "cyan"
        self.imagem_alvo = pygame.image.load("assets/img/target.png")  # Substitua pelo caminho correto
        self.imagem_alvo = pygame.transform.scale(self.imagem_alvo, (self.largura, self.largura))
        self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)
        self.tentativas = Tentativas()
    
    def resetar(self):
        self.x0, self.y0 = 500, 500
        self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)

    def desenhar(self):
        tela.blit(self.imagem_alvo, (self.rect.centerx - self.imagem_alvo.get_width() // 2, self.rect.centery - self.imagem_alvo.get_height() // 2))

    def aleatorizar_posicao(self, objeto:Objeto, nivel):
        """
        Define uma nova posição aleatória para o alvo, evitando colisões com o objeto.
        """
      
        posicao_x = posicao_y = 0
        

        match nivel:
            case 1:
                posicao_x = random.choice([random.uniform(0.25, 0.35), random.uniform(0.65, 0.75)])*LARGURA 
                posicao_y = 0.5*ALTURA
            case 2:
                x_esq = random.randint(int(0.3*LARGURA), int(max(objeto.x - 0.3*LARGURA, 0.3*LARGURA)))
                x_dir = random.randint(int(min(objeto.x + 0.3*LARGURA, 0.8*LARGURA)), int(0.8*LARGURA))


                posicao_x = random.choice([x_dir, x_esq])
                posicao_y = random.choice([0.3, 0.5])*ALTURA 

                if(self.largura > 100):
                    self.largura = self.largura - 10
                    self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)
                    self.imagem_alvo = pygame.transform.scale(self.imagem_alvo, (self.largura, self.largura))
            case 3:
                x_esq = random.randint(int(0.1*LARGURA), int(max(objeto.x - 0.1*LARGURA, 0.1*LARGURA)))
                x_dir = random.randint(int(min(objeto.x + 0.1*LARGURA, 0.9*LARGURA)), int(0.9*LARGURA))

                posicao_x = random.choice([x_dir, x_esq])
                posicao_y = random.choice([0.25, 0.5])*ALTURA

                if(self.largura > 90):
                    self.largura = self.largura - 10
                    self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)
                    self.imagem_alvo = pygame.transform.scale(self.imagem_alvo, (self.largura, self.largura))
            
            case 4:
                x_esq = random.randint(int(0.1*LARGURA), int(max(objeto.x - 0.1*LARGURA, 0.1*LARGURA)))
                x_dir = random.randint(int(min(objeto.x + 0.1*LARGURA, 0.9*LARGURA)), int(0.9*LARGURA))

                posicao_x = random.choice([x_dir, x_esq])
                posicao_y = random.choice([0.25, 0.6])*ALTURA

                if(self.largura > 80):
                    self.largura = self.largura - 5
                    self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)
                    self.imagem_alvo = pygame.transform.scale(self.imagem_alvo, (self.largura, self.largura))
            
            case 5:
                x_esq = random.randint(int(0.2*LARGURA), int(0.3*LARGURA))
                x_dir = random.randint(int(0.7*LARGURA), int(0.9*LARGURA))

                y_cima = random.randint(int(0.2*ALTURA), int(0.3*ALTURA))
                y_baixo = random.randint(int(0.5*ALTURA), int(0.9*ALTURA))


                posicao_x = random.choice([x_dir, x_esq])
                posicao_y = random.choice([y_cima, y_baixo])

                if(self.largura > 70):
                    self.largura = self.largura - 5
                    self.rect = pygame.Rect(self.x0, self.y0, self.largura, self.largura)
                    self.imagem_alvo = pygame.transform.scale(self.imagem_alvo, (self.largura, self.largura))

            case _:
                posicao_x = random.randint(0.1*LARGURA, 0.9*LARGURA)
                posicao_y = random.randint(0.1*ALTURA, 0.9*ALTURA)
        
        self.x0, self.y0 = posicao_x, posicao_y
        self.rect.center = [posicao_x, posicao_y]

    # Checa se o alvo intersecta o objeto
    def checar_proximidade(self, x, y, raio):
        # Coordenadas do alvo
        x_min = self.rect.left
        x_max = self.rect.right
        y_min = self.rect.top
        y_max = self.rect.bottom

        # Encontrar o ponto mais próximo no quadrado
        p_x = max(x_min, min(x, x_max))
        p_y = max(y_min, min(y, y_max))

        # Calcular a distância entre o círculo e o ponto mais próximo
        distancia = math.sqrt((x - p_x)** 2 + (y - p_y)** 2)

        return distancia <= raio
        

# --- Classe Tentativas ---
class Tentativas:
    """
    Representa as tentativas restantes do jogador.
    """
  
    def __init__(self):
        self.tentativas = 0 # Tentativas usadas.
        self.raio = 10 # Raio dos círculos que representam as tentativas na tela.
        self.borda = 1
        self.origem = (30, 30)

    def mostrar(self):
        """
        Exibe os indicadores de tentativas na tela.
        """
        for i in range(0, 3):
            preencher = 0 if i < self.tentativas else self.borda
            pygame.draw.circle(tela, "white", (self.origem[0]*(i+1), self.origem[1]), radius=self.raio, width=preencher)


    
DEBUG = False

# --- Classe Jogo ---
class Jogo:
    """
    Gerencia o fluxo do jogo (estados, pontuação e interação do jogador).
    """
  
    def __init__(self):
        # Lógica do loop do jogo (estados)
    
        self.fundo = pygame.image.load("assets/img/bg.jpg").convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
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

        self.placar = 0 # Pontuação do jogador.
        self.recorde = 0 # Recorde de maior pontuação até o momento.
        self.novo_recorde = False
        self.nivel = 1 # Nível atual.

    #--- Funções auxiliares
    def salvar_recorde(self):
        if not os.path.exists("dados/"):
            os.makedirs("dados/")

        try:
            with open("dados/recorde.bin", "wb+") as arquivo:
                arquivo.write(self.recorde.to_bytes(4, byteorder='big'))
        except (FileNotFoundError, ValueError):
            return 0

    def ler_recorde(self):
        try:
            with open("dados/recorde.bin", "rb") as arquivo:
                return int.from_bytes(arquivo.read(4), byteorder='big')
        except (FileNotFoundError, ValueError):
            return 0
    
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
            self.objeto.velocidade = min(self.objeto.velocidade_maxima, max(0, self.objeto.velocidade+3))
        if keys[pygame.K_DOWN]:
            self.objeto.velocidade = min(self.objeto.velocidade_maxima, max(0, self.objeto.velocidade-3))
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
            mostrar_texto(2, "Acertou!", 0.5*LARGURA,0.9*ALTURA)

        mostrar_texto(1, f"{self.placar}", 60, 80)
        mostrar_texto(2, f"|  Nível {self.nivel}", self.tentativas.origem[0]*5 + 10, self.tentativas.origem[1])

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
        
        mostrar_texto(1, "Pressione para iniciar", 0.5*LARGURA, 0.5*ALTURA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
                self.estado_atual["menu"] = False
            if event.type == pygame.KEYDOWN:
                self.estado_atual["menu"] = False

    def resetar(self):
        self.nivel = math.ceil((self.placar + 1) / 3)

        self.objeto.aleatorizar_posicao(self.nivel)
        self.alvo.aleatorizar_posicao(self.objeto, self.nivel)

        self.tentativas.tentativas = 0

        self.estado_atual["configurar"] = True
        self.proximo_estado = self.configurar


    def configurar(self):
        self.informacoes()
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

        if self.alvo.checar_proximidade(self.objeto.x, self.objeto.y, self.objeto.raio):
            self.estado_atual["jogar"] = False
            self.estado_atual["vitoria"] = True
            self.proximo_estado = self.vitoria

        self.objeto.desenhar_trajetoria(self.t)
        self.objeto.atualizar_posicao(self.t)

        if not self.objeto.naTela() or self.objeto.checar_colisao():
            self.estado_atual["jogar"] = False
            if self.tentativas.tentativas >= 3:
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
        if (self.placar > self.recorde):
            self.recorde = self.placar
            self.salvar_recorde()
            self.novo_recorde = True

        mostrar_texto(2, f"Pressione para continuar", 0.5*LARGURA, 0.10*ALTURA)
        mostrar_texto(1, "Fim de jogo!", 0.5*LARGURA, 0.5*ALTURA, customizado=15)
        mostrar_texto(2, f"Pontuação: {self.placar}", 0.5*LARGURA, 0.60*ALTURA, customizado=30)
        if self.novo_recorde:
            mostrar_texto(3, f"Novo recorde!", 0.5*LARGURA, 0.65*ALTURA, cor="cyan")
        else:
            mostrar_texto(3, f"Recorde: {self.recorde}", 0.5*LARGURA, 0.65*ALTURA)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
            if event.type == pygame.KEYDOWN:
                self.estado_atual["derrota"] = False
        
        if not self.estado_atual["derrota"]:
            self.placar = 0
            self.novo_recorde = False
            self.objeto.x0 = self.objeto.y0 = self.alvo.x0 = self.alvo.y0 = -550
            self.proximo_estado = self.resetar

    def executar_proximo_estado(self):
        """
        Executa o próximo estado do jogo (menu, configurar, jogar, etc.).
        """
        self.proximo_estado()

    #--- Loop do jogo
    def loop(self):
        """
        Loop principal do jogo.
        """
        tela.blit(self.fundo, (0, 0))
        
        self.proximo_estado() # Atualiza o estado atual.

        if (not self.estado_atual["menu"] and not self.estado_atual["configurar"] and not self.estado_atual["derrota"]):
            self.informacoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_jogo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.loop_jogo = False

        pygame.display.update()
        pygame.display.flip()

        clock.tick(120) # Mantém o jogo em 120 FPS.
  

jogo = Jogo()
jogo.recorde = jogo.ler_recorde()

while(jogo.loop_jogo):
    jogo.loop()

if (jogo.placar > jogo.recorde):
    jogo.recorde = jogo.placar
    jogo.salvar_recorde()

pygame.quit()
