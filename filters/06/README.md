# Filtros Morfológicos

# Explicação do Algoritmo de Fechamento Morfológico com Dilatação e Erosão

Este documento explica de forma simples e detalhada o funcionamento de um algoritmo de **fechamento morfológico** em imagens binárias (preto e branco), utilizando duas operações fundamentais do processamento morfológico: **dilatação** e **erosão**. Esse tipo de operação é muito útil para **preencher pequenos buracos** e **conectar regiões brancas separadas por pequenos espaços**.

---

## O que o Algoritmo Faz?

O objetivo do algoritmo é aplicar uma operação de **fechamento morfológico** em uma imagem binária. O fechamento é feito em duas etapas:

1. **Dilatação**: Expande as áreas brancas da imagem.
2. **Erosão**: Encolhe as áreas brancas expandidas, retornando à forma original, mas com pequenas falhas preenchidas.

Essa sequência é usada para **suavizar contornos**, **fechar buracos pequenos** e **juntar componentes próximos** na imagem.

---

## Etapas do Algoritmo

### 1. Binarização da Imagem

Antes de aplicar as operações morfológicas, a imagem é convertida para tons de cinza e em seguida binarizada (preto e branco).

- Cada pixel com valor acima de um certo limiar (ex: 128) se torna **branco (255)**.
- Os demais se tornam **pretos (0)**.

Isso prepara a imagem para as operações morfológicas, que operam melhor em dados binários.

---

### 2. Definição do Kernel (Janela de Vizinhança)

O algoritmo define uma vizinhança 3x3 ao redor de cada pixel. Isso é chamado de **kernel**, e é usado para determinar quais pixels vizinhos serão analisados.

kernel = [(-1, -1), (0, -1), (1, -1),
          (-1,  0), (0,  0), (1,  0),
          (-1,  1), (0,  1), (1,  1)]

Essa estrutura representa os 8 vizinhos ao redor de um pixel, além do próprio pixel central.

---

### 3. Dilatação

A dilatação percorre cada pixel da imagem e examina seus vizinhos dentro do kernel. O valor final do pixel na imagem de saída será o **maior valor encontrado** na vizinhança (ou seja, se houver algum pixel branco perto, o resultado será branco).

#### Objetivo da Dilatação:
- **Expandir as regiões brancas** (objetos) da imagem.
- Preencher pequenos buracos e conectar componentes separados por pequenos espaços.

---

### 4. Erosão

A erosão também percorre cada pixel e sua vizinhança, mas agora ela busca o **menor valor** entre os pixels vizinhos. Se algum pixel preto estiver perto, o resultado será preto.

#### Objetivo da Erosão:
- **Reduzir as regiões brancas**, eliminando expansões indesejadas feitas pela dilatação.
- Após a dilatação, a erosão "encolhe" a forma para recuperar o tamanho original dos objetos, mas mantendo os buracos preenchidos.

---

### 5. Fechamento Morfológico

A operação de **fechamento** consiste em aplicar a **dilatação** seguida de uma **erosão**. No algoritmo: **fechamento = erosão(dilatação(imagem))**

---

#### Resultado Final:
- Pequenas falhas internas nas regiões brancas são **preenchidas**.
- Regiões brancas próximas são **conectadas**.
- A forma geral dos objetos é **mantida**.
