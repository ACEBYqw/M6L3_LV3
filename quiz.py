# quiz.py
import os, json
from config import DATA_DIR, QUIZ_FILE

os.makedirs(DATA_DIR, exist_ok=True)

# Örnek: Türkiye müfredatına uygun bazı sorular
QUIZ_QUESTIONS = {
    "8.sınıf": {
        "Matematik": [
            {"question": "Üslü sayılarda 2^3 = ?", "options": ["6","8","9"], "answer": "8"},
            {"question": "Kareköklü sayı: √49 = ?", "options":["6","7","8"], "answer":"7"}
        ],
        "Fen": [
            {"question": "Su hangi hâlde bulunur?", "options":["Katı","Sıvı","Gaz"], "answer":"Sıvı"}
        ]
    },
    "9.sınıf": {
        "Matematik": [
            {"question": "Fonksiyon: f(x) = 2x, f(3) = ?", "options":["5","6","7"], "answer":"6"}
        ],
        "Fizik": [
            {"question": "Hız formülü nedir?", "options":["v=d/t","F=ma","E=mgh"], "answer":"v=d/t"}
        ]
    },
    "10.sınıf": {
        "Matematik": [
            {"question": "Trigonometri: sin(90°) = ?", "options":["0","1","-1"], "answer":"1"}
        ]
    },
    "11.sınıf": {
        "Matematik": [
            {"question": "Limit: lim x→0 sin(x)/x = ?", "options":["0","1","∞"], "answer":"1"}
        ]
    },
    "12.sınıf": {
        "Matematik": [
            {"question": "Türev: d/dx x^2 = ?", "options":["x","2x","x^2"], "answer":"2x"}
        ]
    }
}

def save_score(user_id, score):
    data = {}
    if os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            try: data = json.load(f)
            except: data = {}
    data[str(user_id)] = score
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
