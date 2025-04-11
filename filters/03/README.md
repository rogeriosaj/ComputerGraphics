# Detecção de bordas

# Explicação do Algoritmo de Detecção de Bordas em Imagens

Este documento explica, de forma simples e detalhada, o funcionamento de um algoritmo de detecção de bordas em imagens. O algoritmo segue uma sequência de etapas clássicas do processamento de imagens, combinando filtros, análise de gradientes e limiares para identificar com precisão as bordas de objetos em uma imagem.

---

## Etapas do Algoritmo

### 1. Conversão para Escala de Cinza (Grayscale)

Antes de processar a imagem, é necessário simplificá-la. A imagem colorida (RGB) é convertida para escala de cinza, pois as cores não são necessárias para detectar bordas. A conversão leva em conta a sensibilidade do olho humano a cada cor, dando mais peso ao verde, seguido do vermelho e depois do azul. Isso gera uma imagem em tons de cinza com valores de 0 (preto) a 255 (branco).

---

### 2. Borramento Gaussiano (Gaussian Blur)

Essa etapa serve para reduzir o ruído na imagem, suavizando as variações abruptas de intensidade. Isso evita que pequenos detalhes ou variações irrelevantes sejam interpretados como bordas. O algoritmo aplica uma média ponderada dos pixels vizinhos (um filtro Gaussiano), priorizando o pixel central, para suavizar a imagem.

---

### 3. Detecção de Bordas com o Filtro de Sobel

O filtro de Sobel é utilizado para identificar mudanças bruscas na intensidade dos pixels — ou seja, bordas. Ele calcula dois gradientes:

- Um na direção horizontal (Gx)
- Outro na direção vertical (Gy)

A partir desses gradientes, o algoritmo determina:
- A intensidade da borda (magnitude do vetor gradiente)
- A direção da borda (ângulo do vetor gradiente)

Isso permite saber não só onde há uma borda, mas também sua orientação.

---

### 4. Supressão Não-Máxima (Non-Maximum Suppression)

Essa etapa refina as bordas detectadas. Muitas vezes, o filtro de Sobel detecta bordas espessas ou duplicadas. A supressão não-máxima analisa a direção da borda e mantém apenas os pixels que representam os pontos mais intensos de cada borda, apagando os demais. Isso deixa as bordas finas e bem definidas.

---

### 5. Limiarização com Histerese (Threshold Hysteresis)

Aqui o algoritmo decide quais bordas são realmente importantes. Ele utiliza dois limiares:

- Um valor alto, para identificar bordas **fortes**
- Um valor baixo, para identificar bordas **fracas**

Bordas fracas só são mantidas se estiverem conectadas a bordas fortes. Isso evita que ruídos e pequenas variações sejam tratados como bordas reais.

---

### 6. Exibição do Resultado

A matriz final, contendo apenas os pixels considerados parte de bordas reais, é convertida novamente em uma imagem para visualização. Essa imagem contém as bordas mais importantes da imagem original, destacadas em branco sobre o fundo preto.