from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import date
from django.utils.dateparse import parse_date


class UserManager(BaseUserManager):
    def create_user(self, cpf, nomeCompleto, password=None):
        """
        Creates and saves a User with the given cpf, date of
        birth and password.
        """
        if not cpf:
            raise ValueError('Users must have an cpf address')

        user = self.model(
            cpf=cpf,
            nomeCompleto=nomeCompleto,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nomeCompleto, password=None):
        """
        Creates and saves a superuser with the given cpf, date of
        birth and password.
        """
        user = self.create_user(
            cpf,
            password=password,
            nomeCompleto=nomeCompleto,
        )
        user.is_admin = True
        user.professor = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    cpf = models.CharField(
        verbose_name='CPF',
        max_length=11,
        unique=True,
    )
    nomeCompleto = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False,verbose_name='Admin')
    professor = models.BooleanField(default=False)
    nomeSocial = models.CharField(blank=True, max_length=100)
    dataNascimento = models.DateField(null=True)
    estado = models.CharField(max_length=2)
    cidade= models.CharField(max_length=100)
    termoUso = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nomeCompleto']

    def __str__(self):
        return self.nomeCompleto

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    @property
    def is_professor(self):
        return self.professor

    @property
    def idade(self):
        value = str(self.dataNascimento)
        age = (date.today() - parse_date(value)).days/365.25
        return int(age)