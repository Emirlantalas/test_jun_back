# Generated by Django 4.2.4 on 2023-08-30 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=16)),
                ('issue_date', models.DateTimeField()),
                ('expiration_date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(max_length=255)),
                ('purchase_date', models.DateTimeField()),
                ('purchase_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.card')),
            ],
        ),
    ]
