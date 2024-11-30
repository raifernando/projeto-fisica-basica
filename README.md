# Lançamento oblíquo
## Descrição básica do jogo 
Este projeto é um jogo em que o jogador controla o ângulo e a velocidade inicial do lançamento de um projétil circular de forma a tentar acertar um alvo que está em uma posição aleatória. Cada acerto é contabilizado e, após três erros, o contador é resetado. O objetivo é conseguir o maior número de acertos, sendo que o recorde é sempre atualizado a cada jogada.

O lançamento do projétil é, na realidade, um caso particular de lançamento oblíquo: um objeto é lançado com um vetor velocidade inicial $$\vec{v_{0}}$$ e, a partir da ação da força de atração gravitacional direcionada ao centro da Terra (força peso), tem sua trajetória determinada. Foi feito, assim, uma modelagem matemática do lançamento e outra para se determinar o vetor $\vec{v_{0}}$, as quais foram implementadas em Python. 

## Modelagem matemática do lançamento oblíquo
Considere um sistema de coordenadas cartesiano bidimensional em que o canto inferior esquerdo da tela é a origem. Sejam $\hat{i}$ e $\hat{j}$ as direções, respectivamente, do eixo $x$ (para a esquerda - sentido positivo) e do eixo $y$ (para cima - sentido positivo). Considere ainda um objeto de massa $m$, lançado da posição $(x_{0}, y_{0})$ (no sistema de coordenadas definido) com um vetor velocidade inicial $\vec{v_{0}}$. Sua posição é denotada por $(x(t), y(t))$, em que $t$ é o parâmetro de tempo.

A fim de simplificações, 	<ins> desconsidera-se a ação da resistência do ar </ins>. Assim, a única força atuante no sistema é a força peso, direcionada verticalmente para baixo. Logo, sendo $\vec{F}$(t) a força resultante e $\vec{F_{g}}(t)$ a força peso, de acordo com a segunda lei de Newton:

$$ \begin{align}
\vec{F}(t) &=  \vec{F_{g}} \\
  m\vec{a}(t) &= -mg\hat{j} \\
  \vec{a}(t) &= -g\hat{j}
 \end{align} $$

 onde $g$ é a constante gravitacional terrestre e $\vec{a}$ é o vetor aceleração do objeto. Seja $(a_{x}(t), a_{y}(t))$ a representação cartesiana de $\vec{a}$. Então $a_{x}(t) = 0$ e $a_{y}(t) = -g$. Portanto, realizando integrações simples:
 
$$ \begin{align}
 v_{x}(t) &= a \\
  v_{y}(t) &= -gt + b \\
 \end{align} $$

 onde v_{x} e v_{y} são as componentes do vetor velocidade ($\vec{v}$), a e b são constantes arbitrárias. Para se determinar essas constantes, são utilizadas as condições iniciais $v_{x}(0) = |\vec{v_{0}}|\cos\theta = v_{0}cos\theta$ e $v_{y} = v_{0}\sin\theta$, em que \theta é o ângulo entre $\vec{v_{0}}$ e o eixo $x$. Assim:

$$ \begin{align}
 v_{x}(t) &= v_{0}\cos\theta \\
  v_{y}(t) &= -gt + v_{0}\sin\theta \\
 \end{align} $$

 Integrando ambas as equações novamente:

 $$ \begin{align}
 x(t) &= v_{0}\cos\theta \cdot t + c \\
  y(t) &= d + v_{0}\sin\theta\cdot t - \displaystyle\frac{gt^{2}}{2} \\
 \end{align} $$

 onde c e d são constantes arbitrárias. Para determiná-las, usam-se as condições iniciais $x(0) = x_{0}$ e $y(0) = y_{0}$, de onde c = x_{0} e d = y_{0}. Logo, a trajetória do projétil é dada pelas equações:

 $$ \fbox{$
 \begin{align} 
 x(t) &= x_{0} + v_{0}\cos\theta \cdot t \\
  y(t) &= y_{0} + v_{0}\sin\theta\cdot t - \displaystyle\frac{gt^{2}}{2} 
  \end{align}
  $}
  $$
 
 


