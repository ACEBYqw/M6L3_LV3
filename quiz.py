import os, json
from config import DATA_DIR, QUIZ_FILE

os.makedirs(DATA_DIR, exist_ok=True)

QUIZ_QUESTIONS = {
    "8.sınıf": {
        "Matematik": [
            {"question": "Üslü sayılarda 2^3 = ?", "options": ["6","8","9"], "answer": "8"},
            {"question": "Kareköklü sayı: √49 = ?", "options":["6","7","8"], "answer":"7"},
            {"question": "Özdeşlikler: (a+b)² = ?", "options":["a²+b²","a²+2ab+b²","a²-b²"], "answer":"a²+2ab+b²"}
        ],
        "Fen Bilimleri": [
            {"question": "Su hangi hâlde bulunur?", "options":["Katı","Sıvı","Gaz"], "answer":"Sıvı"},
            {"question": "DNA'nın yapı birimi nedir?", "options":["Gen","Nükleotit","Kromozom"], "answer":"Nükleotit"},
            {"question": "Basınç birimi nedir?", "options":["Newton","Pascal","Joule"], "answer":"Pascal"}
        ],
        "Türkçe": [
            {"question": "Edat (İlgeç) nedir?", "options":["Tek başına anlamı olan kelime","Cümle kuran kelime","Tek başına anlamı olmayan, cümle içinde anlam kazanan kelime"], "answer":"Tek başına anlamı olmayan, cümle içinde anlam kazanan kelime"},
            {"question": "Fiilde Çatı Kaça Ayrılır?", "options":["2","4","3"], "answer":"2"},
            {"question": "Cümlenin Temel Öğeleri Nedir?", "options":["Özne, Nesne","Yüklem, Nesne","Özne, Yüklem"], "answer":"Özne, Yüklem"}
        ],
        "İngilizce": [
            {"question": "Present Simple Tense'in yardımcı fiilleri nedir?", "options":["Have/Has","Do/Does","Am/Is/Are"], "answer":"Do/Does"},
            {"question": "Must/Mustn't ne ifade eder?", "options":["Gereklilik/Yasak","Olasılık/İzin","Yetki/İstek"], "answer":"Gereklilik/Yasak"},
            {"question": "Which one is a conjunction?", "options":["Beautiful","And","Quickly"], "answer":"And"}
        ],
        "T.C. İnkılap Tarihi": [
            {"question": "Atatürk'ün doğduğu şehir neresidir?", "options":["Ankara","İstanbul","Selanik"], "answer":"Selanik"},
            {"question": "Mondros Ateşkes Antlaşması ne zaman imzalandı?", "options":["1919","1918","1923"], "answer":"1918"},
            {"question": "Kuvâ-yi Milliye nedir?", "options":["Düzenli Ordu","Gönüllü Direniş Güçleri","Saltanat Yanlıları"], "answer":"Gönüllü Direniş Güçleri"}
        ],
    },
    "9.sınıf": {
        "Matematik": [
            {"question": "Fonksiyon: f(x) = 2x, f(3) = ?", "options":["5","6","7"], "answer":"6"},
            {"question": "Mantıkta 'ya da' bağlacının sembolü nedir?", "options":["v","^","⊻"], "answer":"⊻"},
            {"question": "Küme teorisinde A ∩ B ne anlama gelir?", "options":["A veya B'deki elemanlar","A ve B'deki ortak elemanlar","A'nın B'de olmayan elemanları"], "answer":"A ve B'deki ortak elemanlar"}
        ],
        "Fizik": [
            {"question": "Hız formülü nedir?", "options":["v=d/t","F=ma","E=mgh"], "answer":"v=d/t"},
            {"question": "Fizikteki temel büyüklüklere örnek nedir?", "options":["Kuvvet","Enerji","Kütle"], "answer":"Kütle"},
            {"question": "Vektörel büyüklüklere örnek nedir?", "options":["Zaman","Sıcaklık","İvme"], "answer":"İvme"}
        ],
        "Kimya": [
            {"question": "Maddenin en küçük yapı taşı nedir?", "options":["Molekül","Atom","İyon"], "answer":"Atom"},
            {"question": "Kimyasal formülü H₂O olan bileşik nedir?", "options":["Tuz","Amonyak","Su"], "answer":"Su"},
            {"question": "Elementlerin sınıflandırıldığı tabloya ne ad verilir?", "options":["Periyodik Tablo","Cetvel","Spektrum"], "answer":"Periyodik Tablo"}
        ],
        "Biyoloji": [
            {"question": "Canlıların temel bileşenleri nelerdir?", "options":["Mineraller, Proteinler, Yağlar","Su, Organik ve İnorganik Bileşikler","Karbondioksit, Su, Güneş Işığı"], "answer":"Su, Organik ve İnorganik Bileşikler"},
            {"question": "Hücre zarından madde geçişlerine örnek nedir?", "options":["Oksijen Alımı","Mayoz Bölünme","Fotosentez"], "answer":"Oksijen Alımı"},
            {"question": "Canlıların sınıflandırma basamakları nelerdir?", "options":["Tür, Cins, Familya...","Boy, Kilo, Yaş","Renk, Şekil, Koku"], "answer":"Tür, Cins, Familya..."}
        ],
        "Coğrafya": [
            {"question": "Dünya'nın şeklinin sonuçlarına örnek nedir?", "options":["Yerel Saat Farkları","Gelgit Olayı","Yaz ve Kış Mevsimleri"], "answer":"Yerel Saat Farkları"},
            {"question": "Harita çiziminde kullanılan yöntem nedir?", "options":["Projektör","Projeksiyon","Spektrometre"], "answer":"Projeksiyon"},
            {"question": "Atmosfer katmanları nelerdir?", "options":["Troposfer, Stratosfer, Mezosfer...","Okyanus, Deniz, Göl","Kıtalar, Adalar, Yarımadalar"], "answer":"Troposfer, Stratosfer, Mezosfer..."}
        ],
    },
    "10.sınıf": {
        "Matematik": [
            {"question": "Trigonometri: sin(90°) = ?", "options":["0","1","-1"], "answer":"1"},
            {"question": "Polinomlarda P(x) = x² + 1 ise P(2) nedir?", "options":["3","5","4"], "answer":"5"},
            {"question": "İki noktadan geçen doğru denklemi nasıl bulunur?", "options":["Eğim ve bir nokta formülü","Pisagor Teoremi","Limit alma"], "answer":"Eğim ve bir nokta formülü"}
        ],
        "Edebiyat": [
            {"question": "Divan Edebiyatında en çok kullanılan nazım birimi nedir?", "options":["Dörtlük","Beyit","Bent"], "answer":"Beyit"},
            {"question": "Roman türünün kurucusu kabul edilen yazar kimdir?", "options":["Cervantes","Şekspir","Homeros"], "answer":"Cervantes"},
            {"question": "Masalın ana karakteri genellikle nedir?", "options":["Tarihi kişilik","Sıradan insan","Olağanüstü varlık"], "answer":"Olağanüstü varlık"}
        ],
        "Fizik": [
            {"question": "Elektriksel potansiyel enerji formülü nedir?", "options":["E=mc²","U=kQq/r","F=ma"], "answer":"U=kQq/r"},
            {"question": "Basit harmonik hareketin periyodu neye bağlıdır?", "options":["Genlik","Kütle","Yay sabiti ve kütle"], "answer":"Yay sabiti ve kütle"},
            {"question": "Manyetik alan birimi nedir?", "options":["Tesla","Volt","Amper"], "answer":"Tesla"}
        ],
        "Kimya": [
            {"question": "Mol kavramında Avogadro sayısı kaçtır?", "options":["6,02x10²³","1,6x10⁻¹⁹","3x10⁸"], "answer":"6,02x10²³"},
            {"question": "Kimyasal türler arası etkileşimlere örnek nedir?", "options":["London Kuvvetleri","Kütle Çekimi","Radyoaktivite"], "answer":"London Kuvvetleri"},
            {"question": "Çözünürlüğü etkileyen faktörler nelerdir?", "options":["Sıcaklık, Basınç, Ortak İyon","Hacim, Kütle, Yoğunluk","Renk, Koku, Tat"], "answer":"Sıcaklık, Basınç, Ortak İyon"}
        ],
        "Biyoloji": [
            {"question": "Hücre döngüsünün aşamaları nelerdir?", "options":["Mitoz, Mayoz","İnterfaz, Mitotik Evre","Büyüme, Gelişme, Üreme"], "answer":"İnterfaz, Mitotik Evre"},
            {"question": "Kalıtım birimi nedir?", "options":["Gen","Kromozom","DNA"], "answer":"Gen"},
            {"question": "Mendel'in yasaları neyi inceler?", "options":["Evrim","Kalıtım","Ekoloji"], "answer":"Kalıtım"}
        ],
    },
    "11.sınıf": {
        "Matematik": [
            {"question": "Limit: lim x→0 sin(x)/x = ?", "options":["0","1","∞"], "answer":"1"},
            {"question": "İkinci Dereceden Denklemlerin kökleri arasındaki ilişkiyi veren formül nedir?", "options":["Diskriminant","Vieta Formülleri","Euler Formülü"], "answer":"Vieta Formülleri"},
            {"question": "Logaritma: log₂(8) = ?", "options":["2","3","4"], "answer":"3"}
        ],
        "Fizik": [
            {"question": "Vektörlerin çarpımı neyi ifade eder?", "options":["Skaler ve Vektörel çarpım","Bölme ve Toplama","Çıkarma ve Bölme"], "answer":"Skaler ve Vektörel çarpım"},
            {"question": "Bağıl hareket ne demektir?", "options":["Mutlak hız","Gözlemciye göre hız","Sabit hız"], "answer":"Gözlemciye göre hız"},
            {"question": "Tork (Moment) birimi nedir?", "options":["Joule","Newton","Newton metre"], "answer":"Newton metre"}
        ],
        "Kimya": [
            {"question": "Gaz Yasaları nelerdir?", "options":["Boyle, Charles, Gay-Lussac","Newton, Einstein, Mendel","Ohm, Kirchhoff, Faraday"], "answer":"Boyle, Charles, Gay-Lussac"},
            {"question": "Çözeltilerin Derişimi nasıl ifade edilir?", "options":["Molalite, Molarite, Yüzde Derişim","Hacim, Kütle, Yoğunluk","Sıcaklık, Basınç, Enerji"], "answer":"Molalite, Molarite, Yüzde Derişim"},
            {"question": "Reaksiyon Hızı nasıl hesaplanır?", "options":["Ürünlerin oluşum hızı","Girenlerin tüketim hızı","Her ikisi"], "answer":"Her ikisi"}
        ],
        "Biyoloji": [
            {"question": "Sinir sisteminin temel birimi nedir?", "options":["Kas hücresi","Nöron","Kan hücresi"], "answer":"Nöron"},
            {"question": "Endokrin sistem ne işe yarar?", "options":["Vücut ısısını düzenler","Hormonlarla düzenleme yapar","Kan pompalar"], "answer":"Hormonlarla düzenleme yapar"},
            {"question": "Bağışıklık sisteminin temel görevi nedir?", "options":["Enerji üretimi","Vücudu hastalıklara karşı koruma","Hareket etme"], "answer":"Vücudu hastalıklara karşı koruma"}
        ],
        "Coğrafya": [
            {"question": "Kayaç türleri nelerdir?", "options":["Madenler, Okyanuslar","Püskürük, Tortul, Başkalaşım","Denizler, Göller, Nehirler"], "answer":"Püskürük, Tortul, Başkalaşım"},
            {"question": "İklim tipleri nelerdir?", "options":["Akdeniz, Karasal, Ekvatoral","Sıcak, Soğuk, Ilıman","Kış, Yaz, Bahar"], "answer":"Akdeniz, Karasal, Ekvatoral"},
            {"question": "Türkiye'nin yer şekillerine örnek nedir?", "options":["Dağlar, Platolar, Ovalar","Denizaltı volkanları","Atmosfer katmanları"], "answer":"Dağlar, Platolar, Ovalar"}
        ],
    },
    "12.sınıf": {
        "Matematik": [
            {"question": "Türev: d/dx x^2 = ?", "options":["x","2x","x^2"], "answer":"2x"},
            {"question": "İntegral: ∫x dx = ?", "options":["x²/2 + C","x² + C","2x² + C"], "answer":"x²/2 + C"},
            {"question": "Dizilerde aritmetik dizi nedir?", "options":["Ardışık terimleri oranı sabit olan dizi","Ardışık terimleri farkı sabit olan dizi","Her terimi 1 olan dizi"], "answer":"Ardışık terimleri farkı sabit olan dizi"}
        ],
        "Fizik": [
            {"question": "Planck sabiti neyi temsil eder?", "options":["Işık hızını","Kuantum mekaniğinde temel sabiti","Kütle çekimini"], "answer":"Kuantum mekaniğinde temel sabiti"},
            {"question": "Fotoelektrik olay nedir?", "options":["Işıkla elektrik üretimi","Sıcaklık artışı","Manyetik alan oluşumu"], "answer":"Işıkla elektrik üretimi"},
            {"question": "Radyoaktivite birimi nedir?", "options":["Joule","Becquerel","Volt"], "answer":"Becquerel"}
        ],
        "Kimya": [
            {"question": "Asit-Baz tepkimelerine örnek nedir?", "options":["Tuzlu su oluşumu","Nötralleşme","Yanma"], "answer":"Nötralleşme"},
            {"question": "Kimyasal denge nedir?", "options":["İleri ve geri tepkime hızlarının eşit olduğu an","Tepkimenin durduğu an","Maddelerin tamamen bittiği an"], "answer":"İleri ve geri tepkime hızlarının eşit olduğu an"},
            {"question": "Organik kimyada alkanların genel formülü nedir?", "options":["CnH₂n","CnH₂n+2","CnH₂n-2"], "answer":"CnH₂n+2"}
        ],
        "Biyoloji": [
            {"question": "Genden Proteine Sentezi aşamaları nelerdir?", "options":["DNA, RNA, Protein","Transkripsiyon, Translasyon","Mayoz, Mitoz"], "answer":"Transkripsiyon, Translasyon"},
            {"question": "Bitkilerde fotosentezin temel amacı nedir?", "options":["Su emmek","Oksijen üretmek","Besin üretmek"], "answer":"Besin üretmek"},
            {"question": "Popülasyon Genetiği neyi inceler?", "options":["Bireylerin özelliklerini","Bir popülasyondaki gen havuzunu","Hücre bölünmesini"], "answer":"Bir popülasyondaki gen havuzunu"}
        ],
        "Felsefe": [
            {"question": "Felsefenin ana disiplinleri nelerdir?", "options":["Mantık, Etik, Estetik","Matematik, Fizik, Kimya","Tarih, Coğrafya, Biyoloji"], "answer":"Mantık, Etik, Estetik"},
            {"question": "Varlığın ne olduğunu inceleyen felsefe dalı nedir?", "options":["Epistemoloji","Ontoloji","Aksiyoloji"], "answer":"Ontoloji"},
            {"question": "Etik neyi inceler?", "options":["Doğru ve yanlış davranışları","Bilginin kaynağını","Güzelliği"], "answer":"Doğru ve yanlış davranışları"}
        ],
    }
}

def load_scores():
    """Skorları JSON dosyasından okur."""
    if os.path.exists(QUIZ_FILE):
        with open(QUIZ_FILE, "r", encoding="utf-8") as f:
            try:
                content = f.read()
                if not content:
                    return {}
                f.seek(0)
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_score(user_id, new_score):
    """
    Kullanıcının skorunu kaydeder.
    Yeni skor, mevcut skordan yüksekse günceller (Sizin kodunuzdaki hata düzeltildi).
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    scores = load_scores()
    
    user_id_str = str(user_id)
    current_best = scores.get(user_id_str, 0)

    if new_score > current_best:
        scores[user_id_str] = new_score
    
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)


def get_top_scores(limit=10):
    """
    En yüksek skorları sıralar ve ilk 'limit' kadarını döndürür. (Bot.py'deki import için eklendi)
    :return: [(user_id, score), ...] şeklinde sıralı liste.
    """
    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    return sorted_scores[:limit]
