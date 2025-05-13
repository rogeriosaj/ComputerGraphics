import cv2
import numpy as np

# 1. Carregar imagem e converter para escala de cinza
img = cv2.imread("images/400.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Aplicar binarização inversa (para que triângulos fiquem brancos)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 3. Detectar contornos
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

triangles = []

for cnt in contours:
    # Aproximar o contorno para reduzir número de pontos
    approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
    
    if len(approx) == 3:  # Triângulo
        area = cv2.contourArea(cnt)
        if area > 100:  # Ignorar pequenos ruídos
            # Calcular centroide do triângulo
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                triangles.append((cx, cy))

# 4. Verificar se encontrou 4 triângulos
if len(triangles) != 4:
    print(f"[ERRO] Foram encontrados {len(triangles)} triângulos em vez de 4.")
else:
    # Ordenar os pontos: top-left, top-right, bottom-right, bottom-left
    triangles = sorted(triangles, key=lambda p: p[1])  # ordenar por Y
    top = sorted(triangles[:2], key=lambda p: p[0])    # ordenar top pela esquerda/direita
    bottom = sorted(triangles[2:], key=lambda p: p[0]) # ordenar bottom pela esquerda/direita

    roi_pts = np.array([top[0], top[1], bottom[1], bottom[0]], dtype='float32')

    # 5. Definir dimensão desejada da ROI retificada
    width, height = 800, 1000  # ajustar conforme necessário
    dst_pts = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype='float32')

    # Calcular matriz de transformação e aplicar warp
    M = cv2.getPerspectiveTransform(roi_pts, dst_pts)
    roi = cv2.warpPerspective(img, M, (width, height))

    cv2.imwrite("roi_detectada.png", roi)
    print("[INFO] ROI extraída e salva como 'roi_detectada.png'.")
