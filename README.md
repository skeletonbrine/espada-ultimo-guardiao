##### A Espada do Último Guardião #####

Um pequeno jogo no formato de text-adventure, desenvolvido em Python utilizando Pygame; destinado a um trabalho de faculdade na disciplina de Programação II.

Neste jogo, o usuário é atribuído a fazer algumas escolhas, que podem acarretar em finais diferentes, combates e interações diferentes; mas claro, de forma bem simplificada.  A proposta é aplicar conceitos de orientação a objetos e interface gráfica de forma acessível e didática, reforçando o aprendizado em sala e incentivando o estudo prático.

##funcionalidades:

- Escolha de alinhamento do protagonista (podendo ser luz, trevas ou neutro), determinado pela cor do quadrado na HUD durante o combate do jogo. Isso irá determinar coisas como: o ataque especial do personagem, de acordo com o alinhamento dele, interação da história com o personagem e também, seu final.
- Sistema de combate simplificado, com ataque básico, especial (que contém modificadores diferentes com base no alinhamento do personagem) e também um sistema de defesa, que trabalha com o atributo def do personagem que é inversamente proporcional à chance de ataque especial do oponente, ou seja, quanto maior a def do personagem, menor a chance dele utilizar um ataque especial contra o jogador.
- Cenários variados, com backgrounds diversos variando de acordo com o ambiente que o jogador se encontra.
- Escolhas, desde alinhamento a decisão do quê fazer na floresta, podem influenciar diretamente na estratégia de abordagem, mas de forma bem simples.

### Instalação do jogo:

Será necessário baixar o arquivo "main.py"; e executá-lo em um interpretador Python no mínimo 3.11. Além disso, também é necessário que haja a dependência o Pygame instalada no interpretador. Por fim, outra observação importante é manter todas as imagens .png no mesmo diretório que o main.py, e com o exato mesmo nome em que se encontram aqui no github.

## Arquivos:

"main.py" - arquivo principal, é o jogo em si.
"assets/" - pasta contendo todos os .png exigidos para que o jogo rode da forma ideal, com os fundos.

##### Autor:
Eduardo Bozzi

