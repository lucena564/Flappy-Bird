from math import sqrt
from random import randint
import numpy as np

# # Example list
# my_list = [3, 8, 2, 7, 1, 8, 4, 6]

# # Find the index of the first maximum value
# first_max_index = max(range(len(my_list)), key=my_list.__getitem__)

# # Exclude the first maximum value and find the index of the second maximum value
# second_max_index = max((i for i, value in enumerate(my_list) if i != first_max_index), key=my_list.__getitem__)

# print("Index of the first maximum value:", first_max_index)
# print("Index of the second maximum value:", second_max_index)

def selecao_natural(rede1, rede2, qtd = 100):
    flag_primeira_geracao = False
    # Preciso criar uma função que vai criar os novos passaros, a partir dos dois melhores.
        # Os melhores passaros são rede1 e rede2
    
    # Uma vez que eu tiver os dois melhores, eu preciso criar uma função que vai gerar os novos passaros.
    # Os novos passaros vão ser gerados mudando os pesos dos dois melhores passaros. Porém será uma mudança aleatória.
    qtd_novos1 = qtd//3
    qtd_novos2 = qtd - qtd_novos1
    qtd_novos3 = qtd - (qtd_novos1 + qtd_novos2)

    novos = []
    for i in range(qtd_novos1):
        # Criar novas redes a partir da rede1
        nova_rede = rede1 # Crio uma nova rede que vai ser uma cópia da rede1
        # Quero acessar os pesos de nova_rede e mudar eles aleatoriamente.
        for camada in nova_rede:
            for neuronio in camada:
                for peso in neuronio.peso:
                    # Quero por uma chance de 10% de mudar o peso
                    chance = randint(0, 5) # Aqui vai determinar a porcentagem de mudança que eu quero por, no caso coloquei 20% (1 chance em 5)
                    if chance == 4: # Escolhi um número aleatório
                        porcentagem_de_mudanca = randint(0, 10)
                        positivo_ou_negativo = randint(0, 1)
                        if positivo_ou_negativo == 0:
                            porcentagem_de_mudanca = -porcentagem_de_mudanca
                        neuronio.peso[peso] += neuronio.peso[peso] + porcentagem_de_mudanca/100

        novos.append(nova_rede)

    for i in range(qtd_novos2):
        # Criar novas redes a partir da rede2
        nova_rede = rede2 # Crio uma nova rede que vai ser uma cópia da rede2
        # Quero acessar os pesos de nova_rede e mudar eles aleatoriamente.
        for camada in nova_rede:
            for neuronio in camada:
                for peso in neuronio.peso:
                    # Quero por uma chance de 10% de mudar o peso
                    chance = randint(0, 10)
                    if chance == 4: # Escolhi um número aleatório
                        porcentagem_de_mudanca = randint(0, 10)
                        positivo_ou_negativo = randint(0, 1)
                        if positivo_ou_negativo == 0:
                            porcentagem_de_mudanca = -porcentagem_de_mudanca
                        neuronio.peso[peso] += neuronio.peso[peso] + porcentagem_de_mudanca/100

        novos.append(nova_rede)

    for i in range(qtd_novos3):
        nova_rede = rede2
        novos.append(nova_rede)

    # Nessa etapa terei duas listas com novas redes, que são cópias das redes 1 e 2, porém com pesos aleatórios mudados um pouco.
    return novos, flag_primeira_geracao

        

    
    


     