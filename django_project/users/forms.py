from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100,)
   password = forms.CharField()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    #phone = forms.CharField()
    #post = forms.Charfield()
    #department =forms.CharField()
    

    class Meta:
        model = User
        fields = [ 'email']#, 'post' , 'department' ,'phone']
