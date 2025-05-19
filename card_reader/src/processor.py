import cv2
import numpy as np

def get_marked_area_coordinates(
        questions=20,
        opt_per_question=5,
        x_start=10, # deslocamento inicial no eixo X, onde começa a primeira alternativa de cada questão
        x_step=81, # distância entre o início de uma alternativa e o início da próxima
        y_step=81, # distância entre as questões
        top_margin=127, # margem surperior a partir do topo da imagem até a primeira questão
        left_margin=98, # margem esquerda a partir da borda até a área útil
        mark_size=35 # tamanho da área das respotas
):
    return [
        [
            (left_margin + x_start + j * x_step, top_margin + i * y_step, mark_size, mark_size)
            for j in range(opt_per_question)
        ]
        for i in range(questions)
    ]
def process_column(image_gray, mark_coords_column, relative_threshold=0.6):
    _, thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return [
        np.argmax(intensity) if (max(intensity) > (sum([i for i in intensity if i != max(intensity)]) / (len(intensity) - 1 + 1e-5)) * (1 + relative_threshold)) else -1
        for intensity in [
            [cv2.countNonZero(thresh[y:y+h, x:x+w]) for (x, y, w, h) in question]
            for question in mark_coords_column
        ]
    ]


def mark_answer(image_gray, mark_coords, answers):
    image_color = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)

    for question_idx, answer_idx in enumerate(answers):
        if answer_idx == -1:
            continue
        x, y, w, h = mark_coords[question_idx][answer_idx]
        cv2.rectangle(image_color, (x, y), (x + w, y + h), (255, 0, 0), 3)

    return image_color

