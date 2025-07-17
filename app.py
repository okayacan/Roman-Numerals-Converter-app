# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
    (1, 'I')
]

# Converter
ROMAN_VALUES = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50,
    'C': 100, 'D': 500, 'M': 1000
}

def int_to_roman(num):
    """Converts an integer to Roman numerals."""
    if not isinstance(num, int) or not (1 <= num <= 3999):
        return "Invalid input. Please enter an integer between 1 and 3999."
    
    roman_numeral = ""
    for value, symbol in ROMAN_MAP:
        while num >= value:
            roman_numeral += symbol
            num -= value
    return roman_numeral

def roman_to_int(roman_str):
    """Converts a Roman numeral to an integer."""
    if not isinstance(roman_str, str):
        return "Invalid input. Please enter a sequence of Roman numerals."
    
    roman_str = roman_str.upper()
    total = 0
    i = 0
    while i < len(roman_str):
        # Check for two-character exceptions (CM, CD, XC, XL, IX, IV)
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
    
    # Check again with the original Roman numeral after conversion (to ensure validity))
    if int_to_roman(total) == roman_str:
        return total
    else:
        return "Invalid Roman numeral format."


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_value = request.form.get('input_value', '').strip()
        convert_type = request.form.get('convert_type')

        if not input_value:
            error = "Please enter a value."
        else:
            if convert_type == 'to_roman':
                try:
                    num = int(input_value)
                    result = int_to_roman(num)
                except ValueError:
                    error = "Invalid number. Please enter an integer."
            elif convert_type == 'to_int':
                result = roman_to_int(input_value)
            else:
                error = "Invalid conversion type."
        
        if isinstance(result, str) and (""Invalid" in result or "Error" in result):
            error = result
            result = None

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    # This part is not used when running behind Gunicorn or Nginx.
    # For local testing only.
    app.run(debug=True, host='0.0.0.0', port=5000)
