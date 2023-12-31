import pygame
import os
import random
import time
# from charles_darwin import *
from IA_flappybird import *

ia_jogando = True

TELA_LARGURA = 500
TELA_ALTURA = 900

# Carregando as imagens que utilizaremos no jogo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEM_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMAGEM_PASSARO

    # Animações da rotação
    ROTACAO_MAXIMA = 25
    VEL_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0 # Quando o passaro se movimentar, agt vai definir o tempo de animação da curva.
                       # S = S0 + V0 * t +- (a*t²)/2
        self.contagem_imagem = 0 # Saber qual imagem estou utilizando.
        self.imagem = self.IMGS[0]

        self.pontos = 0.0 # Pontos para cada passaro.
        self.vivo = True

    def pontuar(self, pontos):
        total = 0
        total = self.pontos + pontos
        return total

    def morreu(self):
        return not self.vivo

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular deslocamento
        self.tempo += 1
        # S = S0 + V0 * t +- at²/2
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Angulo do passaro (fazer a animação)
        if deslocamento < 0 or self.y < (self.altura - 10):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

        else:
            if self.angulo > -60:
                self.angulo -= self.VEL_ROTACAO

    def desenhar(self, tela):
        # Definir qual imagem o passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Se o pássaro tiver caindo ele não vai bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, geracao=0):
    tela.blit(IMAGEM_BG, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Score: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ia_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()

def main(primeira_geracao=True, redes=None):
    # Talvez isso vá para uma função
    ############################################################
    # geracao = 0
    if primeira_geracao:
        if ia_jogando:
            # geracao = 0
            redes = []
            passaros = []
            passaros_save = []
            pontos_passaros = []
            for i in range(100):
                rede = RedeNeural(3, 5, 1)
                redes.append(rede.copy())
                posicao_x = random.randint(30, 230)
                posicao_y = random.randint(200, 500)
                passaros.append(Passaro(posicao_x, posicao_y+30))
                pontos_passaros.append(0)

            # print("Pontuações dos Passaros antes:", [f"{valor:.2f}" for valor in pontos_passaros])

        else:
            passaros = [Passaro(230, 350)]

    else:
        if ia_jogando:
            passaros = []
            passaros_save = []

            # Testar
            pontos_passaros = []
            passaro_time = []
            for i in range(100):
                # passaros.append(Passaro(230, 350))
                # Quero sortear um numero entre 200 e 300
                posicao_x = random.randint(30, 230)
                posicao_y = random.randint(200, 500)
                passaros.append(Passaro(posicao_x, posicao_y+30))

            # print("Pontuações dos Passaros antes:", [f"{valor:.2f}" for valor in pontos_passaros])

        else:
            print("\nNão implementado ainda, prestar atenção nas gerações, linha 223")
            return

    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    ############################################################
    rodando = True
    # geracao += 1
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if not ia_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        indicie_cano = 0
        if len(passaros) > 0:
            # Descobrir qual cano olhar
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indicie_cano = 1
        else:
            rodando = False
            break

        # Tomada de decisão dos passaros
        for i, passaro in enumerate(passaros):
            # Só quero fazer isso para os passaros que estão vivos.
            if passaro.vivo:
                passaro.mover()
                passaro.pontos = passaro.pontuar(0.1)

                # ----------------------------- TESTANDO ISSO AQ -----------------------------
                # # Adicione o código da penalidade proporcional aqui
                # altura_media = (canos[indicie_cano].altura + canos[indicie_cano].pos_base) / 2
                # distancia_media = abs(passaro.y - altura_media)
                # penalidade_proporcional = 0.1*(distancia_media / TELA_ALTURA)  # Normalizar para o tamanho da tela
                #
                # # Aplicar penalidade aos pontos do passaro
                # passaro.pontos -= penalidade_proporcional
                # ----------------------------------------------------------------------------

                # pontos_passaros[i] += 0.1

                # Passando a leitura dos sensores
                redes[i].set_sensores(passaro.y, abs(passaro.y - canos[indicie_cano].altura), abs(passaro.y - canos[indicie_cano].pos_base))

                output = redes[i].predict()

                if output > 0.5:
                    passaro.pular()

                chao.mover()

        # Vamos dar pontos aqui
        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaro.morreu()

                    # Salvo os pontos do passaro que morreu e também a rede dele.
                    passaros_save.append([passaro.pontos, redes[i].copy()])

                    passaros.pop(i)
                    redes.pop(i)

                    if ia_jogando:
                        if passaro.vivo:
                            passaro.pontos = passaro.pontuar(-1)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1.0
            canos.append(Cano(600))

            # Olhar aq
            for i, passaro in enumerate(passaros):
                if passaro.vivo:
                    passaro.pontos = passaro.pontuar(5)
                    # pontos_passaros[i] += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                if ia_jogando:
                    passaro.pontos = passaro.pontuar(-2)
                    passaros_save.append([passaro.pontos, redes[i].copy()])
                    passaros.pop(i)
                    redes.pop(i)
                    passaro.morreu()


        desenhar_tela(tela, passaros, canos, chao, pontos) # , geracao)
        #


    # Suspeita que esses pontos estão ficando ordenados no vetor, porque? 
    # print("Pontuações dos Passaros:", [f"{item[0]:.2f}" for item in passaros_save])
    # print("Pontuações dos Passaros:", [f"{value:.2f}" for value in pontos_passaros])
    # print("Número de Redes:", len(passaros_save))

    maior = 0
    # segundo_maior = 0
    # second_max_index = RedeNeural(3, 5, 1)
    first_max_index = RedeNeural(3, 5, 1)

    # Problema
    for item in passaros_save:
        if item[0] > maior:
            first_max_index = item[1]
        # else:
        #    if item[0] > segundo_maior:
        #        second_max_index = item[1]

    redes, primeira_geracao = selecao_natural(first_max_index)#, second_max_index)
    # print(primeira_geracao)
    main(primeira_geracao, redes)

    pontos = 0
    desenhar_tela(tela, passaros, canos, chao, pontos)# , geracao)



if __name__ == '__main__':
    main()