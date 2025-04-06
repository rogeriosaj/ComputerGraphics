from PIL import Image
import math
from tqdm import tqdm

def gaussian(x, sigma):
    return math.exp(-(x ** 2) / (2 * sigma ** 2))

def bilateral(image, diameter, sigma_color, sigma_space):
    width, height = image.size
    pixels = image.load()

    result = Image.new("RGB", (width, height))
    result_pixels = result.load()

    for y in tqdm(range(height), desc="Processing"):
        for x in range(width):
            pixel_value = pixels[x, y]
            r_sum = 0
            g_sum = 0
            b_sum = 0
            w_sum = 0

            for i in range(-diameter, diameter + 1):
                for j in range(-diameter, diameter + 1):
                    nx = x + i
                    ny = y + j
                    if 0 <= nx < width and 0 <= ny < height:
                        r, g, b = pixels[nx, ny]
                        
                        spacial_distance = math.sqrt(i**2 + j**2)

                        color_distance = math.sqrt(
                            (r - pixel_value[0]) ** 2 +
                            (g - pixel_value[1]) ** 2 +
                            (b - pixel_value[2]) ** 2
                        )

                        spacial_weight = gaussian(spacial_distance, sigma_space)
                        color_weight = gaussian(color_distance, sigma_color)
                        weight = spacial_weight * color_weight

                        r_sum += r * weight
                        g_sum += g * weight
                        b_sum += b * weight
                        w_sum += weight

            final_r = int(r_sum / w_sum)
            final_g = int(g_sum / w_sum)
            final_b = int(b_sum / w_sum)
            result_pixels[x, y] = (final_r, final_g, final_b)
    return result


image = Image.open("../image.jpg").convert("RGB")
result = bilateral(image, diameter=5, sigma_color=25, sigma_space=25)
image.show()
result.show()