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
                self.peso[f"{i}"] = np.random.uniform(-1000, 1000)


        self.sensor = None
        self.bias = np.random.uniform(-30, 30)
        self.saida = None


class Camada:
    def __init__(self, quantidade_neuronios, anterior = -1 , incluir_bias=True):
        self.neuronios = [Neuronio(anterior) for _ in range(quantidade_neuronios)] # Cria uma lista com vários neurônios na camada

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

        for i in range(self.qtd_camada_escondida): # 4 - Camada Escondida
            for j in range(self.qtd_sensores):     # 3 - Camada de Entrada - Sensores
                soma += self.camada_entrada.neuronios[j].sensor * self.camada_escondida.neuronios[i].peso[f"{j}"]

            # Vou guardar o resultado de cada neurônio da camada escondida em saída.
            self.camada_escondida.neuronios[i].saida = tanh(soma + self.camada_escondida.neuronios[i].bias) # + self.camada_escondida.neuronios[i].bias

        # Agora vou executar os passos do último neuronio, a da camada de saída:
        for i in range(self.qtd_camada_saida): # 1 - Camada de Saída
            for j in range(self.qtd_camada_escondida):
                soma += self.camada_escondida.neuronios[j].saida * self.camada_saida.neuronios[i].peso[f"{j}"]

            self.camada_saida.neuronios[i].saida = tanh(soma + self.camada_saida.neuronios[i].bias) # + self.camada_saida.neuronios[i].bias


        output = self.camada_saida.neuronios[0].saida + self.camada_saida.neuronios[0].bias

        if output > 0:
            # print(output)
            return output
        else:
            return 0