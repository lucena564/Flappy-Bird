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

class Perceptron(_input, hiden_layers1=[], hiden_layers2=[], output):
    def __init__(self):
        self.weights = []
        self.bias = 1
        self.inputs = []
        self.outputs = []
        self.errors = []
        self.error = 0

