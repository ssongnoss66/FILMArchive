from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label = 'ID',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '아이디를 입력하세요',
            }
        )
    )
    email = forms.EmailField(
        label = 'EMAIL',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
            }
        )
    )
    first_name = forms.CharField(
        label = 'FIRST NAME',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이름을 입력하세요',
            }
        )
    )
    last_name = forms.CharField(
        label = 'LAST NAME',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '성을 입력하세요',
            }
        )
    )
    password1 = forms.CharField(
        label = 'PASSWORD1',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '패스워드를 입력하세요'
            }
        )
    )
    password2 = forms.CharField(
        label = 'PASSWORD2',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '패스워드를 한 번 더 입력하세요'
            }
        )
    )
    image = forms.ImageField(
        label = '이미지',
        required = False,
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label = 'EMAIL',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
            }
        )
    )
    first_name = forms.CharField(
        label = 'FIRST NAME',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '이름을 입력하세요',
            }
        )
    )
    last_name = forms.CharField(
        label = 'LAST NAME',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '성을 입력하세요',
            }
        )
    )
    image = forms.ImageField(
        label = '이미지',
        required = False,
    )
    class Meta():
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'image')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label = 'ID',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '아이디를 입력하세요',
            }
        )
    )
    password = forms.CharField(
        label = 'PASSWORD',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '패스워드를 입력하세요'
            }
        )
    )
    class Meta(AuthenticationForm):
        model = get_user_model()
        fields = ('username', 'password')