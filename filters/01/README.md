# Realce e Ajuste de Intensidade

## Etapas do Algoritmo

### 1. Normalização dos Valores dos Pixels

A imagem original possui valores de pixels entre 0 e 255. Para aplicar a correção de gama corretamente, esses valores são normalizados para o intervalo [0, 1], dividindo cada componente RGB por 255. Isso facilita o uso da função matemática de potência, que espera trabalhar com números reais entre 0 e 1.

---

### 2. Aplicação da Correção de Gama

Com os valores normalizados, o algoritmo aplica a fórmula da correção de gama:
**valor_corrigido = (valor_normalizado)^(1 / γ)**

Esse processo ajusta o brilho da imagem:

- Se **γ > 1**, a imagem se torna **mais escura**
- Se **γ < 1**, a imagem se torna **mais clara**

Essa técnica é usada para compensar diferenças na percepção visual humana e no funcionamento dos monitores.

---

### 3. Remapeamento para o Intervalo de Pixels

Após a correção de gama, os valores dos pixels ainda estão entre 0 e 1. Eles são multiplicados novamente por 255 e convertidos para inteiros (`int`) para que possam ser utilizados em uma imagem comum no formato RGB. O resultado é uma nova imagem corrigida, com o brilho ajustado de acordo com o valor de gama escolhido.

---

### 4. Construção da Nova Imagem

Para cada pixel da imagem original, os canais vermelho, verde e azul são corrigidos individualmente usando a fórmula da gama. O novo pixel corrigido é inserido em uma imagem em branco criada com as mesmas dimensões da original.

---

### 5. Exibição do Resultado

Por fim, a imagem original e a imagem corrigida são exibidas lado a lado. Isso permite uma comparação visual do efeito da correção de gama, demonstrando como a transformação altera o brilho e o contraste da imagem.
