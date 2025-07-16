# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Roma rakamları için sözlükler
# Sayıdan Roma'ya dönüşüm için büyükten küçüğe sıralı
ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
    (1, 'I')
]

# Roma'dan sayıya dönüşüm için
ROMAN_VALUES = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50,
    'C': 100, 'D': 500, 'M': 1000
}

def int_to_roman(num):
    """Bir tam sayıyı Roma rakamlarına dönüştürür."""
    if not isinstance(num, int) or not (1 <= num <= 3999):
        return "Geçersiz giriş. Lütfen 1 ile 3999 arasında bir tam sayı girin."
    
    roman_numeral = ""
    for value, symbol in ROMAN_MAP:
        while num >= value:
            roman_numeral += symbol
            num -= value
    return roman_numeral

def roman_to_int(roman_str):
    """Bir Roma rakamını tam sayıya dönüştürür."""
    if not isinstance(roman_str, str):
        return "Geçersiz giriş. Lütfen bir Roma rakamı dizisi girin."
    
    roman_str = roman_str.upper()
    total = 0
    i = 0
    while i < len(roman_str):
        # İki karakterli özel durumları kontrol et (CM, CD, XC, XL, IX, IV)
        if i + 1 < len(roman_str) and roman_str[i:i+2] in ["CM", "CD", "XC", "XL", "IX", "IV"]:
            if roman_str[i:i+2] == "CM": total += 900
            elif roman_str[i:i+2] == "CD": total += 400
            elif roman_str[i:i+2] == "XC": total += 90
            elif roman_str[i:i+2] == "XL": total += 40
            elif roman_str[i:i+2] == "IX": total += 9
            elif roman_str[i:i+2] == "IV": total += 4
            i += 2
        elif roman_str[i] in ROMAN_VALUES:
            total += ROMAN_VALUES[roman_str[i]]
            i += 1
        else:
            return "Geçersiz Roma rakamı formatı."
    
    # Dönüşüm sonrası orijinal Roma rakamıyla tekrar kontrol et (geçerliliği sağlamak için)
    if int_to_roman(total) == roman_str:
        return total
    else:
        return "Geçersiz Roma rakamı formatı."


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_value = request.form.get('input_value', '').strip()
        convert_type = request.form.get('convert_type')

        if not input_value:
            error = "Lütfen bir değer girin."
        else:
            if convert_type == 'to_roman':
                try:
                    num = int(input_value)
                    result = int_to_roman(num)
                except ValueError:
                    error = "Geçersiz sayı. Lütfen bir tam sayı girin."
            elif convert_type == 'to_int':
                result = roman_to_int(input_value)
            else:
                error = "Geçersiz dönüşüm tipi."
        
        if isinstance(result, str) and ("Geçersiz" in result or "Hata" in result):
            error = result
            result = None

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    # Gunicorn veya Nginx arkasında çalışırken bu kısım kullanılmaz.
    # Sadece yerel testler için.
    app.run(debug=True, host='0.0.0.0', port=5000)
