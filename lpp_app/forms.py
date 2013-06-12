# coding: utf-8
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Osada, Handel
from django.utils.html import strip_tags


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Imie'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nazwisko'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Użytkownik'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Potwierdzenie hasła'}))

    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Użytkownik'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class OsadaForm(forms.ModelForm):
    nazwa = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nazwa osady'}))
    class Meta:
        model = Osada        
        fields = ('nazwa', )



class HandelForm(forms.ModelForm):

    class Meta:
        model = Handel  
        fields = ('surowiec1', 'ilosc1', 'surowiec2', 'ilosc2')      

    def __init__(self, *args, **kwargs):
        super(HandelForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

        #self.fields['surowiec1'].empty_label = None
        #self.fields['surowiec2'].empty_label = None
