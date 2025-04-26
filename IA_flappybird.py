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
import numpy as np
import random         # <— importe o módulo, não só funções isoladas
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


def selecao_natural(rede1, rede2, flag_peso_aleatorio_ruim=False, qtd=100):
    """
    Rede1 e Rede2 são os dois melhores da geração.
    Retorna: lista de 'qtd' redes para a próxima geração e flag_primeira_geracao=False.
    """
    novos = []
    flag_primeira_geracao = False

    # 1) Elitismo: pais originais
    novos.append(rede1.copy())
    novos.append(rede2.copy())

    # 2) Determine quantos filhos via crossover e quantos via mutação pura
    n_crossover = qtd // 2 - 1   # metade menos 1 (já contei 2 pais)
    n_mutacao1  = qtd // 4       # um quarto vindo de mutação de rede1
    n_mutacao2  = qtd - 2 - n_crossover - n_mutacao1

    def crossover_uniforme(p1, p2):
        filho = deepcopy(p1)
        for camada in ['camada_escondida', 'camada_saida']:
            cp1 = getattr(p1, camada).neuronios
            cp2 = getattr(p2, camada).neuronios
            cf  = getattr(filho, camada).neuronios
            for n1, n2, nf in zip(cp1, cp2, cf):
                for chave in n1.peso:
                    if random.random() < 0.5:          # aqui
                        nf.peso[chave] = n1.peso[chave]
                    else:
                        nf.peso[chave] = n2.peso[chave]
                nf.bias = n1.bias if random.random() < 0.5 else n2.bias  # e aqui
        return filho

    def mutacao_gaussiana(r, intensidade=0.1):
        """Aplica ruído gaussiano proporcional nos pesos e bias."""
        for camada in ['camada_escondida', 'camada_saida']:
            for n in getattr(r, camada).neuronios:
                for chave in n.peso:
                    sigma = abs(n.peso[chave]) * intensidade
                    n.peso[chave] += np.random.randn() * sigma
                # bias
                sigma_b = abs(n.bias) * intensidade
                n.bias += np.random.randn() * sigma_b

    # 3) Filhos por crossover
    for _ in range(n_crossover):
        filho = crossover_uniforme(rede1, rede2)
        mutacao_gaussiana(filho, intensidade=0.05)  # pequena mutação pós-crossover
        novos.append(filho)

    # 4) Filhos por mutação pura de cada pai
    for _ in range(n_mutacao1):
        filho = deepcopy(rede1)
        mutacao_gaussiana(filho, intensidade=0.2)
        novos.append(filho)

    for _ in range(n_mutacao2):
        filho = deepcopy(rede2)
        mutacao_gaussiana(filho, intensidade=0.2)
        novos.append(filho)

    # 5) Se os pais forem “ruins”, injetar algumas redes totalmente novas
    if flag_peso_aleatorio_ruim:
        n_novas = qtd  # 100% de novas
        from IA_flappybird import RedeNeural
        novos = []
        for _ in range(n_novas):
            novos.append(RedeNeural(3, 5, 1))

    # 6) Ajuste final: se temos mais que qtd, corte; se menos, copie pais até chegar
    if len(novos) > qtd:
        novos = novos[:qtd]
    else:
        while len(novos) < qtd:
            novos.append(deepcopy(rede1))

    return novos, flag_primeira_geracao