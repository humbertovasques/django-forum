# Generated by Django 4.1.4 on 2022-12-31 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF')),
                ('nomeCompleto', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('professor', models.BooleanField(default=False)),
                ('nomeSocial', models.CharField(blank=True, max_length=100)),
                ('dataNascimento', models.DateField(null=True)),
                ('estado', models.CharField(max_length=2)),
                ('cidade', models.CharField(max_length=100)),
                ('termoUso', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]