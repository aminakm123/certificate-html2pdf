# Generated by Django 4.2.3 on 2023-07-20 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfcertificate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='id',
        ),
        migrations.AlterField(
            model_name='certificate',
            name='verification_code',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
