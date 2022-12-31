from django.db import models
from django.contrib.auth.models import (
     AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin,
)
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.contrib import auth

class UserManager(BaseUserManager):
    def create_user(self, cpf, nomeCompleto, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not cpf:
            raise ValueError('Usuários devem ter um CPF')

        user = self.model(
            # email=self.normalize_email(email),
            nomeCompleto=nomeCompleto,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, cpf, nomeCompleto, password=None):
        """
        Creates and saves a staff user with the given cpf and password.
        """
        user = self.create_user(
            cpf,
            password=password,
            nomeCompleto=nomeCompleto,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nomeCompleto, password=None):
        """
        Creates and saves a superuser with the given cpf and password.
        """
        user = self.create_user(
            cpf,
            password=password,
            nomeCompleto=nomeCompleto,
        )
        user.staff = True
        user.admin = True
        user.nomeCompleto = nomeCompleto
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    cpf = models.CharField(
        verbose_name='CPF',
        max_length=11,
        unique=True,
    )
    nomeCompleto = models.CharField(max_length=100)
    nomeSocial = models.CharField(blank=True, max_length=100)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False, verbose_name='Professor') # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    dataNascimento = models.DateField(null=True)
    estado = models.CharField(max_length=100)
    cidade= models.CharField(max_length=100)
    termoUso = models.BooleanField(default=False)

    objects = UserManager()
    
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nomeCompleto'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.nomeCompleto

    def get_short_name(self):
        # The user is identified by their email address
        return self.nomeSocial

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
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

# class UsuarioManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, cpf, password, **extra_fields):
#         """
#         Create and save a user with the given cpf, email, and password.
#         """
#         if not cpf:
#             raise ValueError("The given cpf must be set")
#         # Lookup the real model class from the global app registry so this
#         # manager method can be used in migrations. This is fine because
#         # managers are by definition working on the real model.
#         GlobalUserModel = apps.get_model(
#             self.model._meta.app_label, self.model._meta.object_name
#         )
#         user = self.model(cpf=cpf, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, cpf, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(cpf, password, **extra_fields)

#     def create_superuser(self, cpf, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not  True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(cpf, password, **extra_fields)
    
#     def with_perm(
#         self, perm, is_active=True, include_superusers=True, backend=None, obj=None
#     ):
#         if backend is None:
#             backends = auth._get_backends(return_tuples=True)
#             if len(backends) == 1:
#                 backend, _ = backends[0]
#             else:
#                 raise ValueError(
#                     "You have multiple authentication backends configured and "
#                     "therefore must provide the `backend` argument."
#                 )
#         elif not isinstance(backend, str):
#             raise TypeError(
#                 "backend must be a dotted import path string (got %r)." % backend
#             )
#         else:
#             backend = auth.load_backend(backend)
#         if hasattr(backend, "with_perm"):
#             return backend.with_perm(
#                 perm,
#                 is_active=is_active,
#                 include_superusers=include_superusers,
#                 obj=obj,
#             )
#         return self.none()
    
# class Usuario(AbstractBaseUser):
#     # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     username = None
#     nomeCompleto = models.CharField(max_length=100)
#     nomeSocial = models.CharField(blank=True, max_length=100)
#     cpf = models.CharField(unique=True, max_length=11)
#     dataNascimento = models.DateField(null=True)
#     estado = models.CharField(max_length=100)
#     cidade= models.CharField(max_length=100)
#     termoUso = models.BooleanField(default=False)
#     is_staff = models.BooleanField(
#         _("Professor"),
#         default=False,
#         help_text=_("Designa o usuário como professor do fórum"),
#     )
#     is_active = models.BooleanField(
#         _("Usuário ativo"),
#         default=True,
#         help_text=_(
#             "Ativa ou desativa a conta do usuário"
#         ),
#     )
#     objects =  UserManager()

#     USERNAME_FIELD = "cpf"
#     REQUIRED_FIELDS = ["nomeCompleto"]
    
#     def __str__(self):
#         return self.nomeCompleto

      
