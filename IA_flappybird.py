# Sobre a IA:
"""
    input:
        - Posição Y do Pássaro (distância até o chão).
        - Distância do Pássaro ao cano de cima.
        - Distância do Pássaro ao cano de baixo.

    output:
        - Espaço (um pulo no ar).
"""

from math import sqrt
from random import randint
import numpy as np
from copy import deepcopy


def relu(x):
    return np.maximum(0, x)


def tanh(x):
    return np.tanh(x)


class Neuronio:
    def __init__(self, anterior):
        if (anterior == -1):
            self.peso = None
        else:
            # preciso criar um dicionário para guardar os meus pesos.
            self.peso = {}
            for i in range(anterior):
                self.peso[f"{i}"] = np.random.uniform(-100, 100)

        self.sensor = None
        self.bias = np.random.uniform(-30, 30)
        self.saida = None


class Camada:
    def __init__(self, quantidade_neuronios, anterior=-1, incluir_bias=True):
        self.neuronios = [Neuronio(anterior) for _ in
                          range(quantidade_neuronios)]  # Cria uma lista com vários neurônios na camada

        # if incluir_bias:
        #     self.neuronios.append(Neuronio())  # Adiciona o neurônio de viés
        #
        # self.quantidade_neuronios = quantidade_neuronios + 1 if incluir_bias else quantidade_neuronios


class RedeNeural:
    def __init__(self, sensores=3, camada_escondida=4, camada_saida=1, incluir_bias=False):
        self.camada_entrada = Camada(sensores)
        self.qtd_sensores = sensores

        self.camada_escondida = Camada(camada_escondida, sensores)
        self.qtd_camada_escondida = camada_escondida

        self.camada_saida = Camada(camada_saida, camada_escondida, incluir_bias)
        self.qtd_camada_saida = camada_saida

        self.flag_bias = incluir_bias

    def copy(self):
        return deepcopy(self)

    def set_sensores(self, altura, dist1, dist2):
        self.camada_entrada.neuronios[0].sensor = altura
        self.camada_entrada.neuronios[1].sensor = dist1
        self.camada_entrada.neuronios[2].sensor = dist2

    def predict(self):
        # No futuro preciso fazer de forma recursiva, mas por enquanto vou fazer de forma manual.
        soma = 0

        for i in range(self.qtd_camada_escondida):  # 4 - Camada Escondida
            for j in range(self.qtd_sensores):  # 3 - Camada de Entrada - Sensores
                soma += self.camada_entrada.neuronios[j].sensor * self.camada_escondida.neuronios[i].peso[f"{j}"]

            # Vou guardar o resultado de cada neurônio da camada escondida em saída.
            self.camada_escondida.neuronios[i].saida = tanh(
                soma + self.camada_escondida.neuronios[i].bias)  # + self.camada_escondida.neuronios[i].bias

        # Agora vou executar os passos do último neuronio, a da camada de saída:
        for i in range(self.qtd_camada_saida):  # 1 - Camada de Saída
            for j in range(self.qtd_camada_escondida):
                soma += self.camada_escondida.neuronios[j].saida * self.camada_saida.neuronios[i].peso[f"{j}"]

            self.camada_saida.neuronios[i].saida = tanh(
                soma + self.camada_saida.neuronios[i].bias)  # + self.camada_saida.neuronios[i].bias

        output = self.camada_saida.neuronios[0].saida + self.camada_saida.neuronios[0].bias

        if output > 0:
            # print(output)
            return output
        else:
            return 0


def selecao_natural(rede1, qtd=100):
    flag_primeira_geracao = False
    # Preciso criar uma função que vai criar os novos passaros, a partir dos dois melhores.
    # Os melhores passaros são rede1 e rede2

    # Uma vez que eu tiver os dois melhores, eu preciso criar uma função que vai gerar os novos passaros.
    # Os novos passaros vão ser gerados mudando os pesos dos dois melhores passaros. Porém será uma mudança aleatória.
    qtd_novos1 = qtd  # // 2
    qtd_novos2 = qtd - qtd_novos1
    # qtd_novos3 = qtd - (qtd_novos1 + qtd_novos2)

    novos = []
    # novos.append(rede1)
    # qtd -= 1
    # novos.append(rede2)
    # qtd -= 2
    for i in range(100):
        # Criar novas redes a partir da rede1
        nova_rede = deepcopy(rede1)  # Copia a rede1

        # Quero acessar os pesos de nova_rede e mudar eles aleatoriamente.
        for i in range(nova_rede.qtd_camada_escondida):  # 4 - Camada Escondida
            for j in range(nova_rede.qtd_sensores):      # 3 - Camada de Entrada - Sensores
                # Quero interar sob a chave de pesos do dicionario peso
                for chave_pesos in nova_rede.camada_escondida.neuronios[i].peso:
                    porcentagem_de_mudanca = randint(0, 100)
                    positivo_ou_negativo = randint(0, 1)
                    if positivo_ou_negativo == 0:
                        porcentagem_de_mudanca = -porcentagem_de_mudanca
                    nova_rede.camada_escondida.neuronios[i].peso[chave_pesos] = nova_rede.camada_escondida.neuronios[i].peso[chave_pesos] + (nova_rede.camada_escondida.neuronios[i].peso[chave_pesos])*porcentagem_de_mudanca / 100

        # novos.append(nova_rede)

        # Preciso criar um laço que mude o bias dos neurônios da camada escondida
        for i in range(nova_rede.qtd_camada_escondida):
            porcentagem_de_mudanca = randint(0, 15)
            positivo_ou_negativo = randint(0, 1)
            if positivo_ou_negativo == 0:
                porcentagem_de_mudanca = -porcentagem_de_mudanca
            nova_rede.camada_escondida.neuronios[i].bias = nova_rede.camada_escondida.neuronios[i].bias + (nova_rede.camada_escondida.neuronios[i].bias)*(porcentagem_de_mudanca / 100)

        novos.append(nova_rede)

    # Nessa etapa terei duas listas com novas redes, que são cópias das redes 1 e 2, porém com pesos aleatórios mudados um pouco.
    return novos, flag_primeira_geracao
