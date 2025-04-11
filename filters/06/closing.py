from PIL import Image

kernel = [(-1, -1), (0, -1), (1, -1),
          (-1,  0), (0,  0), (1,  0),
          (-1,  1), (0,  1), (1,  1)]

def dilate(image):
    width, height = image.sizd()
    input_pixels = image.load()
    output = Image.new("L", (width, height), 0)
    output_pixels = output.load()

    for y in range(height):
        for x in range(width):
            max_val = 0
            for dx, dy in kernel:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if input_pixels[nx, ny] > max_val:
                        max_val = input_pixels[nx,ny]
            output_pixels[x,y] = max_val
    return output

def erode(image):
    width, height = image.size
    input_pixels = image.load()
    output = Image.new("L", (width, height), 255)
    output_pixels = output.load()

    for y in range(height):
        for x in range(width):
            min_val = 255
            for dx, dy in kernel:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if input_pixels[nx, ny] < min_val:
                        min_val = input_pixels[nx, ny]
            output_pixels[x, y] = min_val

    return output

def closing(image):
    dilated = dilate(image)
    closed = erode(dilated)
    return closed

image = Image.open("../image.jpg").convert("L")

blackAndWhite = image.point(lambda p: 255 if p > 128 else 0)

closedImage = closing(blackAndWhite)
closedImage.show()
image.show()