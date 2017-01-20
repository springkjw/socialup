# -*-coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from accounts.models import MyUser, Seller, SellerAccount, seller_type_list, Withdrawal
from allauth.account.forms import (
    # SignupForm,
    BaseSignupForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    # SetPasswordField,
    PasswordField,
)
from allauth.account.adapter import get_adapter
from allauth.account.utils import filter_users_by_email
from allauth.socialaccount.models import SocialAccount


class SetPasswordField(PasswordField):
    def __init__(self, *args, **kwargs):
        super(SetPasswordField, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        value = get_adapter().clean_password(value)
        return value


class SignupForm(BaseSignupForm):
    password1 = PasswordField(label="비밀번호")
    password2 = PasswordField(label="비밀번호 확인")

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
                'placeholder': '비밀번호(6자리 이상)'
            }
        )
        self.fields['password1'].error_messages['required'] = '비밀번호를 입력해주세요'
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호 확인'
            }
        )
        self.fields['password2'].error_messages['required'] = '비밀번호 확인을 입력해주세요'

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError("비밀번호가 서로 다릅니다. 확인 부탁드립니다.")
        return cleaned_data

    def raise_duplicate_email_error(self):
        email = self.cleaned_data['email']

        # 페이스북 계정이 이미 있는 경우
        is_social = SocialAccount.objects.filter(user__email=email).exists()
        if is_social:
            raise forms.ValidationError("페이스북으로 연결된 계정입니다. 페이스북 로그인을 이용해 주세요.")
        else:
            raise forms.ValidationError("이미 가입된 이메일입니다.")

    def custom_signup(self, request, user):
        password = self.cleaned_data["password1"]
        user.set_password(password)
        user.save()


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
        fields = ('media', 'name', 'phone', 'description', 'job',
                  'sex', 'address', 'birth_year', 'agree_purchase_info_email',
                  'agree_purchase_info_SMS', 'agree_selling_info_email',
                  'agree_selling_info_SMS', 'agree_marketing_info_email',
                  'agree_marketing_info_SMS')


class ChangeSellerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ChangeSellerForm, self).__init__(*args, **kwargs)

        # widgets
        self.fields['type'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}),choices=seller_type_list)

        # labels
        self.fields['type'].label = '판매 회원 유형'
        self.fields['company_name'].label = '회사명'
        self.fields['representative_name'].label = '대표자명'
        self.fields['corporate_number'].label = '사업자 번호'
        self.fields['business_field'].label = '업태'
        self.fields['company_type'].label = '종목'
        self.fields['business_license'].label = '사업자등록증 사본'
        self.fields['account_copy'].label = '사업자 통장 사본'



    class Meta:
        model = Seller
        fields = ('type', 'company_name', 'representative_name',
                  'corporate_number', 'business_field', 'company_type',
                  'business_license', 'account_copy')


class ChangeSellerAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ChangeSellerAccountForm, self).__init__(*args, **kwargs)

        self.fields['account_name'].label = '예금주'
        self.fields['bank'].label = '은행'
        self.fields['account_number'].label = '계좌번호'

    class Meta:
        model = SellerAccount
        fields = ('account_name', 'bank', 'account_number',)
        widgets = {
            'account_number': forms.TextInput(
                attrs={
                    'placeholder': 'ex) 000-000-000'
                }
            ),
        }



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


class ResetPasswordKeyForm(ResetPasswordKeyForm):
    password1 = SetPasswordField(label="새 비밀번호")
    password2 = PasswordField(label="새 비밀번호 확인")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        self.user = kwargs['user']
        self.temp_key = kwargs.pop("temp_key", None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        if ("password1" in self.cleaned_data
            and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError("비밀번호가 서로 다릅니다. 다시 확인해주세요.")
        return self.cleaned_data["password2"]

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])


class WithdrawalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(WithdrawalForm, self).__init__(*args, **kwargs)

        self.fields['money'].label = '출금액'

    class Meta:
        model = Withdrawal
        fields = ('money', )