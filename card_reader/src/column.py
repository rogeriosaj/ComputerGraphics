import cv2
import os

def find_columns(image_path, candidate_id, out_folder):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erro ao ler imagem: {image_path}")
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilated = cv2.dilate(edged, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = h / float(w)
            if w > 50 and h > 200 and aspect_ratio > 2:
                rects.append((x, y, w, h))

    rects = sorted(rects, key=lambda r: r[0])

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    col_paths = []
    for i, (x, y, w, h) in enumerate(rects):
        col_img = image[y:y+h, x:x+w]
        col_path = os.path.join(out_folder, f'{candidate_id}_col{i+1}.png')
        cv2.imwrite(col_path, col_img)
        col_paths.append(col_path)

    if len(col_paths) == 0:
        print(f"Erro ao detectar coluna em: {image_path}")

    return col_paths