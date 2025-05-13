import cv2
import numpy as np
import os

def detectar_roi(imagem_path):
    """Detecta a ROI a partir de triângulos e retorna a imagem retificada."""
    img = cv2.imread(imagem_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    triangles = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:  # Triângulo
            area = cv2.contourArea(cnt)
            if area > 100:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    triangles.append((cx, cy))

    if len(triangles) != 4:
        print(f"[ERRO] {imagem_path}: Foram encontrados {len(triangles)} triângulos em vez de 4.")
        return None

    triangles = sorted(triangles, key=lambda p: p[1])
    top = sorted(triangles[:2], key=lambda p: p[0])
    bottom = sorted(triangles[2:], key=lambda p: p[0])
    
    roi_pts = np.array([top[0], top[1], bottom[1], bottom[0]], dtype='float32')
    width, height = 800, 1000
    dst_pts = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype='float32')

    M = cv2.getPerspectiveTransform(roi_pts, dst_pts)
    return cv2.warpPerspective(img, M, (width, height))

def dividir_blocos(roi):
    """Divide a ROI em 3 blocos sem salvar os arquivos."""
    h, w = roi.shape[:2]
    bloco_w = w // 3
    blocos = [roi[:, i * bloco_w:(i + 1) * bloco_w] for i in range(3)]
    return blocos

def detectar_respostas_blocos(bloco, questao_inicial):
    """Detecta quais bolhas foram marcadas em um bloco de 20 questões."""
    respostas = {}
    gray = cv2.cvtColor(bloco, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    h, w = thresh.shape
    linhas, colunas = 20, 5
    linha_h = h // linhas
    coluna_w = w // colunas

    for i in range(linhas):
        questao_num = questao_inicial + i
        intensidades = [cv2.countNonZero(thresh[i * linha_h:(i+1) * linha_h, j * coluna_w:(j+1) * coluna_w]) for j in range(colunas)]
        indice_marcado = np.argmax(intensidades)
        respostas[questao_num] = chr(ord('A') + indice_marcado)

    return respostas

def processar_todos_arquivos(pasta):
    """Processa os 498 arquivos e salva os resultados em um arquivo txt."""
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".jpg")]
    arquivos = sorted(os.listdir(pasta), key=lambda x: int(x.split(".")[0]))[:498]

    respostas_gerais = {}

    for idx, arquivo in enumerate(arquivos):
        print(f"[INFO] Processando {arquivo} ({idx+1}/{len(arquivos)})...")
        imagem_path = os.path.join(pasta, arquivo)
        roi = detectar_roi(imagem_path)
        if roi is None:
            continue
        
        blocos = dividir_blocos(roi)
        respostas_total = {}

        for i, bloco in enumerate(blocos):
            respostas_total.update(detectar_respostas_blocos(bloco, i * 20 + 1))

        respostas_gerais[arquivo] = respostas_total

    # Salvar resultados no arquivo txt
    with open("resultados.txt", "w") as f:
        for arquivo, respostas in respostas_gerais.items():
            f.write(f"\n[RESULTADOS] {arquivo}:\n")
            for q, resp in respostas.items():
                f.write(f"Questão {q}: {resp}\n")

    print("[INFO] Processamento concluído. Resultados salvos em 'resultados.txt'.")

# Executar processamento
pasta_imagens = "images"
processar_todos_arquivos(pasta_imagens)
