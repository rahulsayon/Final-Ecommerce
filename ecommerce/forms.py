from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    fullname = forms.CharField( widget=forms.TextInput(attrs={
                                                "class" : "form-control",
                                                "placeholder" : "Fullname"
                                             }) )
    email = forms.CharField(widget=forms.TextInput(attrs={
                                          "class" : "form-control",
                                          "placeholder" : "Email"
                                        }))
    content = forms.CharField(widget=forms.Textarea(attrs={
                                                'class' : "form-control",
                                                "placeholder" : "Enter Your Content"
                                            }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "gmail.com" not in email:
            raise forms.ValidationError("Please enter gmail.com")
        return email
    
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={ "class" : "form-control" }))
    password = forms.CharField( widget=forms.PasswordInput(attrs={ 'class' : "form-control" }))
    
    
    
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={ "class" : "form-control" }))
    email = forms.CharField(widget=forms.TextInput(attrs={ "class" : "form-control" }))
    password = forms.CharField( widget=forms.PasswordInput(attrs={ 'class' : "form-control" }))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={ 'class' : "form-control" }))
    
    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password must be same")
        return password
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = User.objects.filter(username= username)
        if obj.exists():
            raise forms.ValidationError("Username is already taken")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = User.objects.filter(email= email)
        if obj.exists():
            raise forms.ValidationError("Email is already taken")
        return email
        
        