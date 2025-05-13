import cv2
import numpy as np

def detectar_respostas_blocos(imagem_bloco, questao_inicial):
    """
    Detecta quais bolhas foram marcadas em um bloco de 20 questões.
    Retorna um dicionário {n_questao: letra_marcada}
    """
    respostas = {}
    bloc = cv2.imread(imagem_bloco)
    gray = cv2.cvtColor(bloc, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    h, w = thresh.shape
    linhas = 20
    colunas = 5  # A a E

    linha_h = h // linhas
    coluna_w = w // colunas

    for i in range(linhas):
        questao_num = questao_inicial + i
        intensidades = []

        for j in range(colunas):
            x = j * coluna_w
            y = i * linha_h
            cell = thresh[y:y+linha_h, x:x+coluna_w]

            # Calcular a intensidade média dos pixels brancos
            intensidade = cv2.countNonZero(cell)
            intensidades.append(intensidade)

        # A bolha mais escura (maior valor invertido) é considerada marcada
        indice_marcado = np.argmax(intensidades)
        letra = chr(ord('A') + indice_marcado)
        respostas[questao_num] = letra

    return respostas

# Exemplo de uso com os três blocos
respostas_total = {}
respostas_total.update(detectar_respostas_blocos("bloco_1.png", 1))
respostas_total.update(detectar_respostas_blocos("bloco_2.png", 21))
respostas_total.update(detectar_respostas_blocos("bloco_3.png", 41))

for q, resp in respostas_total.items():
    print(f"Questão {q}: {resp}")
