from PIL import Image

def gamma_correction(image, gamma):

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

image = Image.open("../image.jpg").convert("RGB")

gamma = 2.5
final_image = gamma_correction(image, gamma)

image.show()
final_image.show()