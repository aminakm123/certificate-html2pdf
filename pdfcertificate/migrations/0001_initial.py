# Generated by Django 4.2.3 on 2023-07-20 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subtitle', models.TextField()),
                ('date', models.DateField()),
                ('sign', models.CharField(max_length=100)),
                ('verification_code', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'certificate',
                'verbose_name_plural': 'certificates',
                'db_table': 'certificate_certificate',
            },
        ),
    ]