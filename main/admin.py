from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from main.models import User
estados_brasileiros = [
('AC','Acre'),
('AL','Alagoas'),
('AP','Amapá'),
('AM','Amazonas'),
('BA','Bahia'),
('CE','Ceará'),
('DF','Distrito Federal'),
('ES','Espírito Santo'),
('GO','Goiás'),
('MA','Maranhão'),
('MT','Mato Grosso'),
('MS','Mato Grosso do Sul'),
('MG','Minas Gerais'),
('PA','Pará'),
('PB','Paraíba'),
('PR','Paraná'),
('PE','Pernambuco'),
('PI','Piauí'),
('RJ','Rio de Janeiro'),
('RN','Rio Grande do Norte'),
('RS','Rio Grande do Sul'),
('RO','Rondônia'),
('RR','Roraima'),
('SC','Santa Catarina'),
('SP','São Paulo'),
('SE','Sergipe'),
('TO','Tocantins')
]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['cpf','password']

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)
    estado = forms.ChoiceField(choices= estados_brasileiros)
    class Meta:
        model = User
        fields = ['nomeCompleto','nomeSocial','cpf','dataNascimento','estado','cidade','termoUso']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    estado = forms.ChoiceField(choices= estados_brasileiros)

    class Meta:
        model = User
        fields = ['cpf', 'password', 'nomeCompleto', 'is_active', 'is_admin','nomeSocial','dataNascimento','estado','cidade','termoUso']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['nomeCompleto', 'cpf', 'is_admin','professor']
    list_filter = []
    fieldsets = [
        (None, {'fields': ['cpf', 'password']}),
        ('Personal info', {'fields': ['nomeCompleto','nomeSocial','dataNascimento','estado','cidade']}),
        ('Permissions', {'fields': ['is_admin','professor']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['nomeCompleto','nomeSocial','cpf', 'dataNascimento', 'estado','cidade', 'password1', 'password2','is_admin','professor', 'termoUso'],
        }),
    ]
    search_fields = ['cpf','nomeCompleto']
    ordering = ['nomeCompleto']
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
