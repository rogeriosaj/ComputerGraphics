# Transformações Geométricas

# Explicação do Algoritmo de Rotação de Imagem com Remapeamento Inverso

Este documento explica de forma simples e detalhada o funcionamento de um algoritmo de **rotação de imagem** utilizando a técnica de **remapeamento inverso (reverse mapping)**. Essa técnica é mais precisa que métodos simples de rotação e evita problemas comuns como buracos ou distorções.

---

## O que o Algoritmo Faz?

O objetivo do algoritmo é **rotacionar uma imagem** em torno de seu centro, utilizando um ângulo fornecido pelo usuário. Em vez de mover os pixels da imagem original para suas novas posições, o algoritmo faz o inverso: **para cada pixel da imagem de saída, calcula de onde ele veio na imagem original**.

---

## Etapas do Algoritmo

### 1. Cálculo do Centro da Imagem

A rotação acontece ao redor do centro da imagem. Por isso, o algoritmo calcula:

- `cx` = centro horizontal
- `cy` = centro vertical

Esses valores são usados para aplicar a rotação com relação ao centro, e não ao canto superior esquerdo da imagem.

---

### 2. Conversão do Ângulo para Radianos

Como funções trigonométricas em Python trabalham com radianos, o ângulo fornecido em graus é convertido usando a fórmula: **theta = math.radians(angle)**

Em seguida, calcula-se o seno e cosseno de `theta` para uso posterior.

---

### 3. Remapeamento Inverso (Reverse Mapping)

O ponto-chave do algoritmo é que, em vez de calcular **"para onde vai cada pixel da imagem original"**, ele calcula **"de onde vem cada pixel da imagem de saída"**.

Para cada pixel `(x, y)` da imagem de saída:

- Translada-se o ponto para a origem (subtraindo o centro)
- Aplica-se a rotação inversa com os valores de seno e cosseno
- Translada-se de volta ao sistema de coordenadas da imagem original

Se a coordenada de origem (`src_x`, `src_y`) estiver dentro dos limites da imagem original, o valor do pixel é copiado. Caso contrário, o pixel recebe cor preta `(0, 0, 0)`.

---

## Vantagens do Remapeamento Inverso

- **Evita buracos na imagem**: cada pixel da imagem de saída é garantidamente preenchido.
- **Melhor controle da interpolação** (neste caso, usa arredondamento simples, mas poderia ser melhorado).
- **Preserva o tamanho da imagem** original.

---

## Considerações

- O algoritmo pode ser melhorado utilizando interpolação bilinear para suavizar a imagem rotacionada.
- O fundo preto aparece porque o algoritmo não tenta preencher os espaços "vazios" após a rotação.
