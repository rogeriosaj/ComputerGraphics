import os
import pandas as pd
import cv2

from .column import find_columns
from .processor import process_column, mark_answer, get_marked_area_coordinates

def process(images, marked_answers, columns, processed):
    question_per_column = 20

    os.makedirs(marked_answers, exist_ok=True)
    os.makedirs(columns, exist_ok=True)

    marked_coords_column = get_marked_area_coordinates(questions=question_per_column)
    data = []

    for candidate_id, file in enumerate(sorted(f for f in os.listdir(images) if f.lower().endswith('.jpg')), start=1):
        path = os.path.join(images, file)
        columns_path = find_columns(path, candidate_id, out_folder=columns)

        all_answers_column = [
            answer
            for idx_col, column_path in enumerate(columns_path)
            for answer in process_column(cv2.imread(column_path, cv2.IMREAD_GRAYSCALE), marked_coords_column)
        ]

        # Marca e salva as imagens das colunas
        for idx_col, column_path in enumerate(columns_path):
            image_gray = cv2.imread(column_path, cv2.IMREAD_GRAYSCALE)
            answers = process_column(image_gray, marked_coords_column)
            marked_image = mark_answer(image_gray, marked_coords_column, answers)
            marked_column_name = f'{candidate_id}_col{idx_col+1}.png'
            marked_column_path = os.path.join(marked_answers, marked_column_name)
            cv2.imwrite(marked_column_path, marked_image)

        data.extend({
            'questao': i,
            'resposta': chr(65 + idx_resp) if idx_resp != -1 else '',
            'candidato': candidate_id
        } for i, idx_resp in enumerate(all_answers_column, start=1))

    pd.DataFrame(data).to_csv(processed, sep=';', index=False)