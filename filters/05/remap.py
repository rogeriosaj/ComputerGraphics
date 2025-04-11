from PIL import Image
import math

def rotationRemap(image, angle):
    width, height = image.size
    cx, cy = width / 2, height / 2

    # Angulo para radianos
    theta = math.radians(angle)
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)

    input_pixels = image.load()
    output_image = Image.new("RGB", (width, height), color=(0,0,0))
    output_pixels = output_image.load()

    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy

            # Rotacao reversa
            src_x = cos_theta * dx + sin_theta* dy + cx
            src_y = sin_theta * dx + cos_theta * dy + cy

            src_x_int = int(round(src_x))
            src_y_int = int(round(src_y))

            if 0 <= src_x_int < width and 0 <=src_y_int < height:
                output_pixels[x,y] = input_pixels[src_x_int, src_y_int]
            else:
                output_pixels[x,y] = (0,0,0)
    return output_image

image = Image.open("../image.jpg")
rotated = rotationRemap(image, 30)
image.show()
rotated.show()            