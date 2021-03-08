from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from .models import Userprofile
from django.utils.translation import ugettext_lazy as _

class UserprofileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserprofileForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['class'] = 'input'
        self.fields['zipcode'].widget.attrs['class'] = 'input'
        self.fields['place'].widget.attrs['class'] = 'input'
        self.fields['phone'].widget.attrs['class'] = 'input'
    class Meta:
        model = Userprofile
        fields = '__all__'
        exclude = ('user',)

        labels = {
            "address": _("Адреса:"),
            "zipcode": _("Поштенски број:"),
            "place": _("Град:"),
            "phone": _("Телефон:"),
            
        }

        widgets = {
        'address': forms.fields.TextInput(attrs={'placeholder': 'Вашата адреса'}),
        'place': forms.fields.TextInput(attrs={'placeholder': 'Град'}),
        'zipcode': forms.fields.TextInput(attrs={'placeholder': 'Поштенски број'}),
        'phone': forms.fields.TextInput(attrs={'placeholder': 'Телефонски број за контакт'}),
    }       
        



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True , label="Име:",widget=forms.TextInput(attrs={ 'placeholder': 'Име'}))
    last_name = forms.CharField(max_length=50, required=True,label="Презиме:",widget=forms.TextInput(attrs={ 'placeholder': 'Презиме'}))
    email = forms.EmailField(max_length=255, required=True, label="Емаил:",widget=forms.TextInput(attrs={ 'placeholder': 'Емаил'}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Лозинка'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторете ја лозинката'}))

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("емаил адресата постои")
        return self.cleaned_data['email']

    def clean_email(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("корисничкото име постои")
        return self.cleaned_data['username']

    
    


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['password1'].label = 'Лозинка:'
        self.fields['password2'].label = 'Повторете ја лозинката:'

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''

        

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['first_name'].widget.attrs['class'] = 'input'
        self.fields['last_name'].widget.attrs['class'] = 'input'
        

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
        'username': forms.fields.TextInput(attrs={'placeholder': 'Вашето Корисничко име'})
    }        
        
            
        
        labels = {
            "username": _("Корисничко име"),
        }

        

        