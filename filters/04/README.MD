# Detecção de Formas e Texturas

# Explicação do Algoritmo de Filtro de Gabor em Imagens

Este documento explica de forma simples e detalhada o funcionamento de um algoritmo que aplica o **filtro de Gabor** em uma imagem. Esse filtro é muito utilizado em processamento de imagens e visão computacional para detectar **texturas**, **padrões** e **orientações específicas**.

---

## O que é o Filtro de Gabor?

O **filtro de Gabor** combina uma função Gaussiana com uma onda senoidal. Isso permite destacar regiões com frequência espacial específica e orientação definida. Ele é muito útil para detectar **bordas orientadas**, **texturas** e **padrões repetitivos**.

---

## Etapas do Algoritmo

### 1. Geração do Kernel de Gabor

A primeira etapa é construir um **kernel 2D** com base nos seguintes parâmetros:

- **`ksize`**: Tamanho do kernel (deve ser ímpar, como 21).
- **`sigma`**: Desvio padrão da gaussiana (define a largura do filtro).
- **`theta`**: Orientação do filtro, em radianos (por exemplo, π/4 para 45 graus).
- **`lambd`**: Comprimento de onda da onda senoidal (define a frequência).
- **`gamma`**: Razão de aspecto da gaussiana (define a elipticidade).
- **`phi`**: Fase da onda senoidal.

O kernel gerado possui valores que respondem fortemente a regiões da imagem que possuem **padrões alinhados** com a orientação (`theta`) e frequência (`lambd`) definidas.

---

### 2. Aplicação do Kernel sobre a Imagem

Com o kernel criado, o algoritmo percorre a imagem pixel por pixel (ignorando as bordas) e aplica uma **convolução** com o kernel de Gabor. Isso significa multiplicar cada pixel vizinho por um valor do kernel e somar tudo. O resultado é uma nova imagem onde padrões específicos (como texturas em uma certa direção) são destacados.

---

### 3. Exibição do Resultado

A imagem final mostra apenas as regiões que “responderam” bem ao filtro — ou seja, que possuem características semelhantes ao que o kernel foi configurado para detectar. Regiões com texturas ou bordas alinhadas à orientação escolhida aparecerão em destaque.

---

## Aplicações

- Detecção de **textura** em imagens médicas.
- Extração de **características faciais** (como sobrancelhas e rugas).
- Análise de **digitais**.
- Detecção de **bordas em direções específicas**.

