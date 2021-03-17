from django import forms

class LogInForm(forms.Form):
    id = forms.EmailField(label='아이디', max_length=20)
    pw = forms.CharField(label='암  호', max_length=30, widget=forms.PasswordInput)