import numpy as np
import cv2

def gamma_correction(image, gamma):
    # Etapa 1-> normalizar a imagem
    nImage = image / 255.0

    # Etapa 2-> aplicar a correçao de gama
    cImage = np.power(nImage, 1 / gamma) # np.power calcula a^b para cada elemento

    # Etapa 3-> conversao para imagem comum, pixel original
    finalImage = np.uint8(cImage * 255.0)

    return finalImage

image = cv2.imread("./01.jpg")

gamma = 2.5
corrected_image = gamma_correction(image, gamma)
cv2.imshow("Original Image", image)
cv2.imshow("Gamma Corrected Image", corrected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()