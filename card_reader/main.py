from variables import SOURCE, ANSWERS, MARKED_ANSWERS, COLUMNS, PROCESSED, COMPARISON
from src.answer_csv import process
from src.compare import results

def main():
    process(SOURCE, MARKED_ANSWERS, COLUMNS, PROCESSED)
    results(PROCESSED, ANSWERS, COMPARISON)

if __name__ == '__main__':
    main()
