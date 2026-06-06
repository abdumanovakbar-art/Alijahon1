import re

from django.contrib.auth import forms, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms import ModelForm, CharField


from apps.models import User


class LoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)



    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def clean(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = re.sub(r'\D', '', phone_number)

        password = self.cleaned_data['password']

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise ValidationError("Telefon raqam topilmadi")
        if not check_password(password, user.password):
            raise ValidationError("Parol xato kiritildi")
        login(self.request, user)
        return self.cleaned_data



class RegistrationForm(ModelForm):
    conf_password = CharField(max_length=50)
    class Meta:
        model = User
        fields = ['phone_number', 'password', 'conf_password']

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise Exception("Parol kamida 4 ta belgidan iborat bo'lishi kerak!!")
        hash_password = make_password(password)
        return hash_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = re.sub(r'\D', '', phone_number)
        return phone_number

    def clean_conf_password(self):
        conf_password = self.cleaned_data['conf_password']
        password = self.data['password']
        if conf_password != password:
            raise Exception('Confirm password xato kiritilgan!')