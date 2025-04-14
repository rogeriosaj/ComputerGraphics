# Redução de Ruído e Suavização

## Etapas do Algoritmo

### 1. Conceito do Filtro Bilateral

O filtro bilateral é uma técnica avançada de suavização de imagem que preserva as bordas. Diferente de filtros tradicionais (como o Gaussiano), ele considera **duas dimensões** ao calcular o peso de cada pixel vizinho:

- **Distância espacial**: quão longe o pixel vizinho está do pixel central.
- **Distância de cor**: quão diferente em cor o pixel vizinho está do pixel central.

Com isso, o filtro consegue suavizar regiões uniformes da imagem **sem borrar as bordas**.

---

### 2. Cálculo das Pesos com Funções Gaussianas

Para cada pixel, o algoritmo percorre uma vizinhança definida por um **diâmetro**. Para cada pixel vizinho dentro dessa janela:

- Calcula a **distância espacial** (`√(i² + j²)`) entre o pixel central e o vizinho.
- Calcula a **distância de cor** entre os valores RGB do pixel central e do vizinho.
- Aplica a **função Gaussiana** para ambas as distâncias, usando os parâmetros `sigma_space` e `sigma_color`.

O peso final é o produto das duas gaussianas:
**peso = gauss(espacial) * gauss(cor)**

---

### 3. Aplicação dos Pesos

O algoritmo acumula os valores ponderados de cada componente de cor (R, G, B) com base no peso calculado:

- Soma ponderada dos valores dos vizinhos
- Soma total dos pesos aplicados

Após percorrer todos os vizinhos, os novos valores de R, G e B são obtidos pela divisão entre a soma ponderada e a soma dos pesos.

---

### 4. Criação da Nova Imagem

Para cada pixel, é calculado um novo valor RGB com base na média ponderada, e esse valor é inserido em uma nova imagem. O processo se repete até que todos os pixels da imagem original sejam processados.

---

### 5. Exibição do Resultado

A imagem original e a imagem filtrada são exibidas. O resultado é uma imagem suavizada que mantém as bordas nítidas, sendo ideal para pré-processamento em tarefas de segmentação ou detecção de características.
