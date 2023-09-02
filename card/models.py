from django.db import models
from datetime import datetime, timedelta
import random
import string



class Card(models.Model):
    owner_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    issue_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)


    def generate_card_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


    def calculate_expiration_date(self):

        return self.issue_date + timedelta(days=365)


    def save(self, *args, **kwargs):

        if not self.card_number:
            self.card_number = self.generate_card_number()


        if not self.expiration_date:
            self.expiration_date = self.calculate_expiration_date()

        super(Card, self).save(*args, **kwargs)


class Purchase(models.Model):
    seller_name = models.CharField(max_length=255)
    purchase_date = models.DateTimeField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    card = models.ForeignKey('card.Card', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.seller_name} ({self.purchase_date})"


