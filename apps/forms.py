import re
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, Form
from django.forms.fields import CharField, IntegerField, ChoiceField
from django.views.generic import FormView
from pydantic_core import ValidationError
from apps.models import User, Transaction


class UserModel(ModelForm):
    confirm_password = CharField(max_length=50)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5:
            raise ValidationError('Password uzunligi yetarli emas !')
        hash_passeord = make_password(password)
        return hash_passeord

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        phone_number = re.sub(r'\D', '', phone_number)
        return phone_number

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.data['password']
        if confirm_password != password:
            raise ValidationError('Parol xato!')



class PayForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['card_number', 'amount', 'type']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Summa 0 dan katta bo'lishi kerak!")
        return amount



class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telegram_id', 'description' , ]




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

