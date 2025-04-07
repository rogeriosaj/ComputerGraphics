from PIL import Image
from tqdm import tqdm
import math

def generater_kernel_gabor(ksize, sigma, theta, lambd, gamma, phi):
    kernel = []
    half = ksize // 2

    for y in range(-half, half + 1):
        line = []
        for x in range(-half, half + 1):
            x_prime = x * math.cos(theta) + y * math.sin(theta)
            y_prime = -x * math.sin(theta) + y * math.cos(theta)

            gauss = math.exp(-(x_prime**2 + (gamma**2) * y_prime**2) / (2 * sigma**2))
            sinus = math.cos(2 * math.pi * x_prime / lambd + phi)

            value = gauss * sinus
            line.append(value)
        kernel.append(line)
    return kernel

def apply_kernel(image, kernel):
    width, height = image.size
    pixels = image.load()
    output = Image.new("L", (width, height))
    output_pixels = output.load()

    ksize = len(kernel)
    offset = ksize // 2

    for y in tqdm(range(offset, height - offset), desc="Aplicando filtro Gabor"):
        for x in range(offset, width - offset):
            soma = 0
            for ky in range(ksize):
                for kx in range(ksize):
                    px = x + kx - offset
                    py = y + ky - offset
                    soma += pixels[px, py] * kernel[ky][kx]
            value = int(min(max(soma, 0), 255))
            output_pixels[x, y] = value
    return output


ksize = 21        # Tamanho do kernel (ímpar)
sigma = 4.0       # Desvio padrão da gaussiana
theta = math.pi / 4  # Orientação (ex: pi/4 para 45°)
lambd = 10.0      # Comprimento de onda
gamma = 0.5       # Razão de aspecto
phi = 0           # Fase

image = Image.open("../image.jpg").convert("L")  # Image em escala de cinza
kernel = generater_kernel_gabor(ksize, sigma, theta, lambd, gamma, phi)
result = apply_kernel(image, kernel)

image.show()
result.show()
