from django import forms
from django.contrib.auth.password_validation import validate_password

from customuser.models import CustomUser


class CustomUserSignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must have letters and numbers. And must be at least 8 characters.'
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(CustomUserSignUpForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this e-email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError({
                'confirm_password': "Passwords don't match."
            })


class CustomUserLoginForm(forms.Form):
    email = forms.CharField(label='E-mail')
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
