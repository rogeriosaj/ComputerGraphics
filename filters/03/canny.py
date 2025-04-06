from PIL import Image
import math
from tqdm import tqdm
import time

def grayscale(image):
    width, heigth = image.size
    gray = Image.new("L", (width, heigth))
    pixels = image.load()
    gray_pixels = gray.load()

    for y in tqdm(range(heigth), desc="Grayscaling"):
        for x in range(width):
            r, g, b = pixels[x, y]
            gray_pixels[x, y] = int(r * 0.299 + g * 0.587 + b * 0.114)
    return gray

def gaussian_blur(image):
    kernel = [
        [1, 4, 6, 4, 1],
        [4, 16, 24, 16, 4],
        [6, 24, 36, 24, 6],
        [4, 16, 24, 16, 4],
        [1, 4, 6, 4, 1]
    ]
    kernel_size = 5
    kernel_sum = sum(map(sum, kernel))
    width, height = image.size
    pixels = image.load()
    output = Image.new("L", (width, height))
    output_pixels = output.load()
    offset = kernel_size // 2
    for y in tqdm(range(offset, height - offset), desc="Gaussian Blurring"):
        for x in range(offset, width - offset):
            acc = 0
            for ky in range(kernel_size):
                for kx in range(kernel_size):
                    pixel_x = x + ky - offset
                    pixel_y = y + ky - offset
                    acc += pixels[pixel_x, pixel_y] * kernel[ky][kx]
            output_pixels[x, y] = int(acc / kernel_sum)
    return output

def sobel(image):
    Gx = [[-1, 0, 1], 
          [-2, 0, 2],
          [-1, 0, 1]]
    Gy = [[1, 2, 1], 
          [0, 0, 0],
          [-1, -2, -1]]
    width, height = image.size
    pixels = image.load()
    magnitude = [[0]*width for _ in range(height)]
    direction = [[0]*width for _ in range(height)]

    for y in tqdm(range(1, height - 1), desc="Sobel Filtering"):
        for x in range(1, width - 1):
            gx = 0
            gy = 0
            for ky in range(3):
                for kx in range(3):
                    px = x + kx - 1
                    py = y + ky - 1
                    val = pixels[px, py]
                    gx += Gx[ky][kx] * val
                    gy += Gy[ky][kx] * val
            magnitude[y][x] = math.hypot(gx, gy)
            direction[y][x] = math.atan2(gy, gx)

    return magnitude, direction

def non_maximum_suppression(magnitude, direction):
    height = len(magnitude)
    width = len(magnitude[0])
    result = [[0]*width for _ in range(height)]

    for y in tqdm(range(1, height - 1), desc="Supressão não-máxima (NMS)"):
        for x in range(1, width - 1):
            angle = direction[y][x] * 180.0 / math.pi
            angle %= 180
            m = magnitude[y][x]
            q = r = 0

            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                q = magnitude[y][x + 1]
                r = magnitude[y][x - 1]
            elif 22.5 <= angle < 67.5:
                q = magnitude[y + 1][x - 1]
                r = magnitude[y - 1][x + 1]
            elif 67.5 <= angle < 112.5:
                q = magnitude[y + 1][x]
                r = magnitude[y - 1][x]
            elif 112.5 <= angle < 157.5:
                q = magnitude[y - 1][x - 1]
                r = magnitude[y + 1][x + 1]

            if m >= q and m >= r:
                result[y][x] = m
            else:
                result[y][x] = 0
    return result

def threshold_hysteresis(image, low, high):
    height = len(image)
    width = len(image[0])
    result = [[0]*width for _ in range(height)]
    strong = 255
    weak = 50

    for y in tqdm(range(height), desc="Aplicando threshold"):
        for x in range(width):
            val = image[y][x]
            if val >= high:
                result[y][x] = strong
            elif val >= low:
                result[y][x] = weak

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if result[y][x] == weak:
                neighbors = [
                    result[y+dy][x+dx]
                    for dy in (-1, 0, 1)
                    for dx in (-1, 0, 1)
                    if not (dx == 0 and dy == 0)
                ]
                if strong in neighbors:
                    result[y][x] = strong
                else:
                    result[y][x] = 0
    return result

def exibir_resultado(matrix):
    height = len(matrix)
    width = len(matrix[0])
    img = Image.new("L", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = int(matrix[y][x])
    img.show()

image = Image.open("../image.jpg")
gray = grayscale(image)
blurred = gaussian_blur(gray)
magnitude, direction = sobel(blurred)
nms = non_maximum_suppression(magnitude, direction)
edges = threshold_hysteresis(nms, low=30, high=100)
exibir_resultado(edges)
image.show()