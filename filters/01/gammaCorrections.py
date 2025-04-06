from PIL import Image
import cv2

def gamma_correction(image, gamma):
    # Etapa 1-> normalizar a imagem
    #    nImage = image / 255.0

    # Etapa 2-> aplicar a correçao de gama
    #    cImage = np.power(nImage, 1 / gamma) # np.power calcula a^b para cada elemento

    # Etapa 3-> conversao para imagem comum, pixel original
    #    finalImage = np.uint8(cImage * 255.0)

    width, height = image.size
    finalImage = Image.new("RGB", (width, height))

    # Função de correção de gama np.power
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            r = int(255 * (r / 255) ** (1 / gamma))
            g = int(255 * (g / 255) ** (1 / gamma))
            b = int(255 * (b / 255) ** (1 / gamma))
            finalImage.putpixel((x, y), (r, g, b))

    return finalImage

#   image = cv2.imread("./01.jpg")
image = Image.open("../image.jpg").convert("RGB")

gamma = 2.5
corrected_image = gamma_correction(image, gamma)
# cv2.imshow("Original Image", image)
# cv2.imshow("Gamma Corrected Image", corrected_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

image.show()
corrected_image.show()