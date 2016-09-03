# -*-coding: utf-8 -*-
from accounts.models import MyUser
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import filter_users_by_email
from django import forms


class SignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': '이메일'
            }
        )
        self.fields['email'].label = '이메일'
        self.fields['email'].error_messages['required'] = '이메일를 입력해주세요'

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호'
            }
        )
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].error_messages['required'] = '비밀번호를 입력해주세요'
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호 확인'
            }
        )
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].error_messages['required'] = '비밀번호 확인을 입력해주세요'

    def raise_duplicate_email_error(self):
        raise forms.ValidationError("이미 가입된 이메일입니다")


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': '이메일'
            }
        )
        self.fields['login'].label = '이메일'
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호'
            }
        )
        self.fields['password'].label = '비밀번호'
        self.fields['remember'].label = '자동로그인'


class ChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ChangeForm, self).__init__(*args, **kwargs)

        self.fields['media'].label = ""
        self.fields['description'].label = "자기소개"
        self.fields['name'].label = "이름"
        self.fields['phone'].label = "연락처"

    class Meta:
        model = MyUser
        fields = ('media', 'name', 'phone', 'description',)


class ResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget = forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': '이메일'
            }
        )
        self.fields['email'].label = '이메일'

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        if not self.users:
            raise forms.ValidationError("가입된 이메일이 없습니다.")
        return self.cleaned_data["email"]
