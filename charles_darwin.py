from math import sqrt
from random import randint
import numpy as np

# Example list
my_list = [3, 8, 2, 7, 1, 8, 4, 6]

# Find the index of the first maximum value
first_max_index = max(range(len(my_list)), key=my_list.__getitem__)

# Exclude the first maximum value and find the index of the second maximum value
second_max_index = max((i for i, value in enumerate(my_list) if i != first_max_index), key=my_list.__getitem__)

print("Index of the first maximum value:", first_max_index)
print("Index of the second maximum value:", second_max_index)

def selecao_natural(passaralho1, passaralho2):
    

     