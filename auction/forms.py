# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from auction.models import User, Brand, Category


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class CreateListingForm(forms.Form):
    name = forms.CharField(max_length=255)
    imageurl = forms.URLField()
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    price = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstName', 'lastName','username', 'dob', 'mobileNo', 'profile_picture', 'address']