import csv

def get_answers(filename):
    all_answers = {}
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            candidate = row['candidato'].strip()
            question = row['questao'].strip()
            answer = row['resposta'].strip().upper()
            if candidate not in all_answers:
                all_answers[candidate] = {}
            all_answers[candidate][question] = answer
    return all_answers

def results(processed, original, comparison):
    
    processed_answers = get_answers(processed)
    original_answers = get_answers(original)

    candidates = sorted(
        set(processed_answers.keys()) | set(original_answers.keys()),
        key=lambda x: int(x)
    )

    with open(comparison, 'w', encoding='utf-8') as result:
        acertos = [
            (
                candidate,
                sum(
                    1 for question in original_answers.get(candidate, {})
                    if question in processed_answers.get(candidate, {})
                    and processed_answers[candidate][question] == original_answers[candidate][question]
                ),
                len(original_answers.get(candidate, {}))
            )
            for candidate in candidates
        ]

        total_hits = sum(hit for _, hit, _ in acertos)
        total_questions = sum(total for _, _, total in acertos)

        for candidate, hit, total in acertos:
            rate = (hit / total * 100) if total > 0 else 0
            result.write(f"ID: {candidate}\n")
            result.write(f"Taxa de acerto: {rate:.2f}%\n\n")

        media_final = (total_hits / total_questions * 100) if total_questions > 0 else 0
        result.write("MÉDIA DE ACERTOS\n")
        result.write(f"{media_final:.2f}%\n")