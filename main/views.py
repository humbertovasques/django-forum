from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from datetime import date
from django.utils.dateparse import parse_date
from .admin import UserCreationForm, LoginForm
from .models import User
from cpf_field.validators import re


def home(request):
    return render(request, 'home.html')

def cadastrarUsuario(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                try: 
                    cpf_is_valid(request.POST['cpf'])
                    try:
                        maior_de_18(request.POST['dataNascimento'])
                        try:
                            newuser = User.objects.create_user(request.POST['cpf'],nomeCompleto=request.POST['nomeCompleto'], password=request.POST['password1'])
                            newuser.termoUso = request.POST['termoUso']
                            newuser.termoUso = newuser.termoUso == 'on'
                            newuser.nomeSocial = request.POST['nomeSocial']
                            newuser.dataNascimento = request.POST['dataNascimento']
                            newuser.estado = request.POST['estado']
                            newuser.cidade = request.POST['cidade']
                            newuser.save()
                            login(request, newuser)
                            return render(request,'home.html',{'success':'Cadastro realizado com sucesso.'})
                        except MultiValueDictKeyError:
                            return render(request,'cadastrarUsuario.html',{'form': UserCreationForm(),'error':'Não foi possível realizar o cadastro. É necessário assinar o termo de uso.'})
                    except ValidationError as ageError:
                        return render(request,'cadastrarUsuario.html',{'form': UserCreationForm(),'error':'Não foi possível realizar o cadastro. ' + ageError.message})
                except ValidationError as cpfError:
                    return render(request,'cadastrarUsuario.html',{'form': UserCreationForm(),'error':'Não foi possível realizar o cadastro. ' + cpfError.message})
            except IntegrityError:
                return render(request,'cadastrarUsuario.html',{'form': UserCreationForm(),'error':'Não foi possível realizar o cadastro. Usuário já existe.'})
        else:
            return render(request,'cadastrarUsuario.html',{'form': UserCreationForm(), 'error':'Não foi possível realizar o cadastro. Senha incorreta.'})
    else:
        return render(request,'cadastrarUsuario.html',{'form': UserCreationForm()})

def loginUsuario(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'loginUsuario.html',{'form': LoginForm(),'error':'CPF ou senha inválidos.'})
        else:
            login(request,user)
            return redirect('home')
    else:
        return render(request,'loginUsuario.html',{'form': LoginForm()})

@login_required
def logoutUsuario(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def digit_generator(cpf, weight):
    sum_digit = 0
    for n in range(weight - 1):
        sum_digit = sum_digit + int(cpf[n]) * weight
        weight = weight - 1

    digit = 11 - sum_digit % 11
    return 0 if digit > 9 else digit

def cpf_is_valid(value):
    isValid = False
    INVALIDS_CPFS = ("11111111111", "22222222222", "33333333333", "44444444444", "55555555555",
                 "66666666666", "77777777777", "88888888888", "99999999999", "00000000000")
    cpf = re.sub("[^0-9]", "", value)
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 números', 'invalid')

    first_digit = digit_generator(cpf, weight=10)

    second_digit = digit_generator(cpf, weight=11)

    if cpf in INVALIDS_CPFS or (not cpf[-2:] == "%s%s" % (first_digit, second_digit)):
        raise ValidationError('Número de CPF inválido', 'invalid')

def maior_de_18(value):
    age = (date.today() - parse_date(value)).days/365.25
    if not age >= 18:
        raise ValidationError('Usuário deve ser maior de 18 anos', 'invalid')
