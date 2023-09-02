import random
import string

def generate_unique_card_number():
    # Генерация уникального номера карты, например, случайной комбинации букв и цифр
    unique_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return unique_number
