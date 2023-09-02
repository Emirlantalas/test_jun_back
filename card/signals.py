from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Card
from datetime import datetime, timedelta
import random


@receiver(pre_save, sender=Card)
def generate_card_number_and_expiration_date(sender, instance, **kwargs):
    if not instance.card_number:
        # Генерируем номер карты (здесь может быть ваша логика)
        instance.card_number = generate_card_number()

    if not instance.expiration_date:
        # Устанавливаем срок окончания активности +1 год от текущей даты
        instance.expiration_date = datetime.now() + timedelta(days=365)


def generate_card_number():
    while True:
        # Генерируем случайный номер карты, состоящий из 16 цифр
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        # Проверяем, уникален ли сгенерированный номер карты
        if not Card.objects.filter(card_number=card_number).exists():
            return card_number

def check_card_expiration(sender, instance, **kwargs):
    if instance.expiration_date and instance.expiration_date < datetime.now().date():
        instance.status = 'просрочена'