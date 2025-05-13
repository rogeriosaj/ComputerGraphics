import cv2
import numpy as np
import pandas as pd
import os

def detectar_roi(img, candidato_id):
    """Improved ROI detection with fallback methods and visualization for debugging"""
    # Save original image for debugging
    debug_img = img.copy()
    
    # Method 1: Try original triangle detection method
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on debug image
    cv2.drawContours(debug_img, contours, -1, (0, 255, 0), 2)
    
    triangles = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3 and cv2.contourArea(cnt) > 100:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                triangles.append((cx, cy))
                # Draw triangle center on debug image
                cv2.circle(debug_img, (cx, cy), 5, (0, 0, 255), -1)
    
    # Save debug image
    os.makedirs("debug", exist_ok=True)
    cv2.imwrite(f"debug/triangle_detection_{candidato_id}.jpg", debug_img)
    
    # If we have 4 triangles, use original method
    if len(triangles) == 4:
        triangles = sorted(triangles, key=lambda p: p[1])  # sort by Y
        top = sorted(triangles[:2], key=lambda p: p[0])    # top-left, top-right
        bottom = sorted(triangles[2:], key=lambda p: p[0]) # bottom-left, bottom-right
        roi_pts = np.array([top[0], top[1], bottom[1], bottom[0]], dtype="float32")
        width, height = 800, 1000
        dst_pts = np.array([[0,0],[width,0],[width,height],[0,height]], dtype="float32")
        M = cv2.getPerspectiveTransform(roi_pts, dst_pts)
        roi = cv2.warpPerspective(img, M, (width, height))
        return roi
        
    # Method 2: Try rectangle detection as fallback
    print(f"[AVISO] Método de triângulos falhou para candidato {candidato_id}, tentando método alternativo...")
    
    # Try to find rectangular shapes
    squares = []
    hierarchy = None  # Make sure we're getting all contours
    
    # Try with different thresholds
    for thresh_val in [50, 100, 150, 200]:
        _, thresh2 = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        contours2, _ = cv2.findContours(thresh2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours2:
            area = cv2.contourArea(cnt)
            if area > 1000:  # Filter out small contours
                approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                if len(approx) == 4:  # Looking for rectangles
                    squares.append(approx)
    
    # Debug rectangle detection
    rect_debug = img.copy()
    cv2.drawContours(rect_debug, squares, -1, (0, 0, 255), 2)
    cv2.imwrite(f"debug/rectangle_detection_{candidato_id}.jpg", rect_debug)
    
    # If we found rectangles, try to use the largest one
    if squares:
        # Get the largest rectangle by area
        largest_rect = max(squares, key=cv2.contourArea)
        rect_pts = largest_rect.reshape(-1, 2)
        
        # Order points: top-left, top-right, bottom-right, bottom-left
        s = rect_pts.sum(axis=1)
        rect_pts = rect_pts[np.argsort(s)]
        rect_pts = rect_pts[[0, 2, 3, 1]]  # Reorder to match expected format
        
        width, height = 800, 1000
        dst_pts = np.array([[0,0],[width,0],[width,height],[0,height]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect_pts.astype(np.float32), dst_pts)
        roi = cv2.warpPerspective(img, M, (width, height))
        return roi
    
    # Method 3: Last resort - try to use the entire image
    print(f"[AVISO] Métodos de detecção falham para candidato {candidato_id}, tentando usar imagem completa...")
    h, w = img.shape[:2]
    # If image is too large, resize while maintaining aspect ratio
    if max(h, w) > 1200:
        scale = 1200 / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h))
    
    # Pad if needed to get closer to expected 800x1000 aspect ratio
    h, w = img.shape[:2]
    target_ratio = 800/1000  # width/height
    img_ratio = w/h
    
    if img_ratio > target_ratio:  # Image too wide
        new_h = int(w / target_ratio)
        pad_top = (new_h - h) // 2
        pad_bottom = new_h - h - pad_top
        img = cv2.copyMakeBorder(img, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    else:  # Image too tall
        new_w = int(h * target_ratio)
        pad_left = (new_w - w) // 2
        pad_right = new_w - w - pad_left
        img = cv2.copyMakeBorder(img, 0, 0, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    # Resize to final dimensions
    roi = cv2.resize(img, (800, 1000))
    return roi

def cortar_blocos(roi):
    h, w = roi.shape[:2]
    bloco_w = w // 3
    blocos = []
    for i in range(3):
        x_start = i * bloco_w
        blocos.append(roi[0:h, x_start:x_start+bloco_w])
    return blocos

def detectar_respostas(bloco, questao_inicial):
    respostas = {}
    gray = cv2.cvtColor(bloco, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    h, w = thresh.shape
    linhas, colunas = 20, 5
    linha_h = h // linhas
    coluna_w = w // colunas
    for i in range(linhas):
        questao = questao_inicial + i
        intensidades = []
        for j in range(colunas):
            x = j * coluna_w
            y = i * linha_h
            cell = thresh[y:y+linha_h, x:x+coluna_w]
            intensidade = cv2.countNonZero(cell)
            intensidades.append(intensidade)
        indice = np.argmax(intensidades)
        letra = chr(ord('A') + indice)
        respostas[questao] = letra
    return respostas

def processar_candidato(imagem_path, df_respostas, missing_candidates=None):
    # Extract candidate ID from filename
    candidato_id = int(os.path.splitext(os.path.basename(imagem_path))[0])
    img = cv2.imread(imagem_path)
    if img is None:
        print(f"[ERRO] Não foi possível carregar {imagem_path}")
        return
    
    roi = detectar_roi(img, candidato_id)
    if roi is None:
        print(f"[ERRO] ROI não detectada para {candidato_id} após todas as tentativas")
        if missing_candidates is not None:
            missing_candidates.append(candidato_id)
        return
    
    # Save ROI for verification
    os.makedirs("output", exist_ok=True)
    cv2.imwrite(f"output/roi_{candidato_id}.jpg", roi)
    
    blocos = cortar_blocos(roi)
    respostas_lidas = {}
    respostas_lidas.update(detectar_respostas(blocos[0], 1))
    respostas_lidas.update(detectar_respostas(blocos[1], 21))
    respostas_lidas.update(detectar_respostas(blocos[2], 41))
    
    # Save responses to file
    with open(f"output/respostas_{candidato_id}.txt", 'w') as f:
        for q in sorted(respostas_lidas.keys()):
            f.write(f"Questão {q}: {respostas_lidas[q]}\n")
    
    # Get responses for this candidate (direct match, knowing the structure)
    respostas_oficiais = df_respostas[df_respostas["candidato"] == candidato_id]
    
    if len(respostas_oficiais) == 0:
        print(f"[AVISO] Nenhuma resposta oficial encontrada para o candidato {candidato_id}")
        if missing_candidates is not None:
            missing_candidates.append(candidato_id)
        return
    
    acertos = 0
    total = len(respostas_oficiais)
    respostas_comparacao = []
    
    for _, row in respostas_oficiais.iterrows():
        try:
            q = int(row["questao"])
            oficial = str(row["resposta"]).strip().upper()
            lida = respostas_lidas.get(q, None)
            match = lida == oficial
            if match:
                acertos += 1
            
            respostas_comparacao.append((q, oficial, lida, match))
        except ValueError:
            print(f"[AVISO] Erro ao processar questão para o candidato {candidato_id}")
            continue
    
    # Save comparison to file
    with open(f"output/comparacao_{candidato_id}.csv", 'w') as f:
        f.write("questao,oficial,lida,match\n")
        for q, oficial, lida, match in sorted(respostas_comparacao):
            f.write(f"{q},{oficial},{lida},{match}\n")
    
    percentual = acertos/total*100 if total > 0 else 0
    print(f"Candidato {candidato_id}: {acertos}/{total} acertos ({percentual:.1f}%)")
    return candidato_id, acertos, total

def main():
    # Check if CSV exists
    csv_path = "respostas.csv"
    if not os.path.exists(csv_path):
        print(f"[ERRO] Arquivo {csv_path} não encontrado!")
        return
    
    # Load CSV - we know the structure is already correct
    try:
        df = pd.read_csv(csv_path)
        print(f"[INFO] CSV carregado com sucesso. Colunas: {df.columns.tolist()}")
        
        # Check if column names match expected values
        expected_columns = ['questao', 'resposta', 'candidato']
        if not all(col in df.columns for col in expected_columns):
            print(f"[AVISO] As colunas do CSV não correspondem às esperadas: {expected_columns}")
            print(f"[AVISO] Colunas encontradas: {df.columns.tolist()}")
        
        # Print candidate statistics
        candidatos_unicos = df['candidato'].unique()
        print(f"[INFO] Total de candidatos no CSV: {len(candidatos_unicos)}")
        print(f"[INFO] Faixa de candidatos: {min(candidatos_unicos)} a {max(candidatos_unicos)}")
        
        # Create a set of available candidates for faster lookup
        candidatos_disponiveis = set(candidatos_unicos)
        
    except Exception as e:
        print(f"[ERRO] Falha ao ler o CSV: {e}")
        return
    
    pasta = "images"
    if not os.path.exists(pasta):
        print(f"[ERRO] Pasta {pasta} não encontrada!")
        return
        
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    if not arquivos:
        print(f"[ERRO] Nenhuma imagem encontrada na pasta {pasta}")
        return
        
    print(f"[INFO] Processando {len(arquivos)} imagens...\n")
    
    # Create output directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("debug", exist_ok=True)
    
    resultados = []
    missing_candidates = []
    
    # Check for missing images before processing
    ids_com_imagens = set()
    for arq in arquivos:
        try:
            id_candidato = int(os.path.splitext(os.path.basename(arq))[0])
            ids_com_imagens.add(id_candidato)
        except ValueError:
            print(f"[AVISO] Nome de arquivo não é um número inteiro: {arq}")
    
    # Find candidates in CSV without images
    candidatos_sem_imagem = candidatos_disponiveis - ids_com_imagens
    if candidatos_sem_imagem:
        print(f"[AVISO] {len(candidatos_sem_imagem)} candidatos no CSV não possuem imagens")
        with open("output/candidatos_sem_imagem.csv", 'w') as f:
            f.write("candidato\n")
            for cand in sorted(candidatos_sem_imagem):
                f.write(f"{cand}\n")
    
    # Find images without candidate data in CSV
    imagens_sem_dados = ids_com_imagens - candidatos_disponiveis
    if imagens_sem_dados:
        print(f"[AVISO] {len(imagens_sem_dados)} imagens não possuem dados de respostas no CSV")
        with open("output/imagens_sem_dados.csv", 'w') as f:
            f.write("candidato\n")
            for cand in sorted(imagens_sem_dados):
                f.write(f"{cand}\n")
    
    # Process all images
    for i, arq in enumerate(arquivos):
        caminho = os.path.join(pasta, arq)
        print(f"[{i+1}/{len(arquivos)}] Processando {arq}...")
        resultado = processar_candidato(caminho, df, missing_candidates)
        if resultado:
            resultados.append(resultado)
    
    # Generate summary statistics if we have results
    if resultados:
        resultados_df = pd.DataFrame(resultados, columns=['candidato', 'acertos', 'total'])
        media_acertos = resultados_df['acertos'].mean()
        media_percentual = (resultados_df['acertos'] / resultados_df['total']).mean() * 100
        
        print("\n===== RESUMO =====")
        print(f"Total de candidatos processados com sucesso: {len(resultados)}")
        print(f"Média de acertos: {media_acertos:.2f}")
        print(f"Média percentual: {media_percentual:.2f}%")
        
        # Save results to CSV
        resultados_df.to_csv("output/resultados_finais.csv", index=False)
        
        # Distribution of scores
        if len(resultados_df) > 0:
            bins = range(0, 101, 10)  # 0-10%, 10-20%, etc.
            percentuais = (resultados_df['acertos'] / resultados_df['total']) * 100
            hist, _ = np.histogram(percentuais, bins=bins)
            
            print("\nDistribuição de notas:")
            for i in range(len(hist)):
                print(f"{bins[i]}-{bins[i+1]}%: {hist[i]} candidatos")
        
        # Missing candidate analysis
        if missing_candidates:
            print(f"\nCandidatos sem respostas oficiais ({len(missing_candidates)}): {missing_candidates[:10]}...")
            with open("output/candidatos_sem_correspondencia.csv", 'w') as f:
                f.write("candidato\n")
                for cand in sorted(missing_candidates):
                    f.write(f"{cand}\n")
        
        print("=================")
        print(f"[INFO] Resultados salvos em output/resultados_finais.csv")
        print(f"[INFO] Detalhes de processamento salvos na pasta 'output'")
        print(f"[INFO] Imagens de diagnóstico salvas na pasta 'debug'")

if __name__ == "__main__":
    main()
