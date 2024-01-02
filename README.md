# Flappy-Bird com IA </br>

<p align="center">
  <a href="https://github.com/lucena564/Flappy-Bird/blob/main/images_gifs_readme/1 File to readme.gif">
    <img src="https://github.com/lucena564/Flappy-Bird/raw/main/images_gifs_readme/1 File to readme.gif" alt="GIF do Flappy Bird" height="300">
  </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/lucena564/Flappy-Bird/blob/main/images_gifs_readme/2 File to readme.gif">
    <img src="https://github.com/lucena564/Flappy-Bird/raw/main/images_gifs_readme/2 File to readme.gif" alt="GIF do Flappy Bird - Ponto Alto" height="300">
  </a>
</p>

Sempre quis colocar em prática os conceitos adquiridos durante meus estudos na área de aprendizado de máquina. </br>

Decidi desenvolver uma Multilayer Perceptron para aprender a jogar o Flappy Bird. </br>

Para isso foi necessário primeiro recriar o jogo do Flappy Bird e depois implementar uma perceptron. 

</br>Para jogar o jogo por conta própria, basta executar o arquivo:</br>
```sh
  $ python flappy_bird_jogo.py
```

 ou    

```sh
  $ python3 flappy_bird_jogo.py
```

</br>A inteligência artificial foi completamente implementada no arquivo:

```sh
  IA_flappybird.py
```

</br> Para observar a IA em treinamento, execute o arquivo:

```sh
  $ python main.py
```

Alguns detalhes que utilizei para esta implementação: </br>
* Utilização de 3 sensores para a camada de entrada. </br>
* 5 neurônios para a camada oculta e 1 neurônio para a camada de saída.</br>
* O Bias presente na camanda escondida e de saída.</br>
* Função de ativação ReLu para todos os neurônios da camada oculta.</br>
* Função de ativação tangente hiperbólica para a camada de saída.</br></br>

Algumas tarefas que farei no futuro:</br>
- [x] Adicionar um requirements.txt
- [x] Organizar o sensor de cada pássaro para a movimentação correta
- [ ] Investigar o motivo de alguns pesos gerarem passaros que vão para full para cima e outros para baixo.
- [ ] Implementar uma estrutura que cria e deixa visível a estrutura da IA (camada de entrada, camada escondida e a camada de saída).
- [ ] Tirar todos os hard coded que deixei.
- [ ] Criar uma lib minha que cria uma nova rede de acordo com o input (x, y, z), sendo x a camada de entrada e y a camada de saída.
- [ ] Determinar a pontuação máxima para parar o treinamento e salvar os pesos. Além disso, criar uma função para carregar os pesos da IA treinada deixando a opção para jogar contra a IA.
- [ ] Verificar e estudar, mostrando um relatório do impacto das diferentes funções de ativações, nas diferentes camadas.
