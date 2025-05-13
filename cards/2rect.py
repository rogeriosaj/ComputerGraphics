import cv2
import numpy as np

# Carregar ROI já retificada
roi = cv2.imread("roi_detectada.png")
h, w = roi.shape[:2]

# Definir número de blocos e dimensões
n_blocos = 3
bloco_w = w // 3

# Cortar e salvar os 3 blocos
for i in range(n_blocos):
    x_start = i * bloco_w
    x_end = x_start + bloco_w

    bloco = roi[0:h, x_start:x_end]
    cv2.imwrite(f"bloco_{i+1}.png", bloco)

print("[INFO] Blocos 1, 2 e 3 salvos como 'bloco_1.png' até 'bloco_3.png'")
