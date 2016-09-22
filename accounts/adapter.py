# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import redirect
from django.contrib import messages
from allauth.account.adapter import (
    app_settings,
    DefaultAccountAdapter,
)
from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter,
)
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.models import EmailAddress
from accounts.models import MyUser


class AccountAdapter(DefaultAccountAdapter):
    # login 후 redirect 페이지
    def get_login_redirect_url(self, request):
        return '/'

    def clean_password(self, password):
        if password is not None:
            min_length = app_settings.PASSWORD_MIN_LENGTH
            if len(password) < min_length:
                error_message = "비밀번호는 %s자리 이상이여야합니다." % (min_length)
                raise forms.ValidationError(error_message)
            return password

    def clean_password2(self, password):
        print password

    def set_password(self, user, password):
        user.set_password(password)
        user.save()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        account = MyUser.objects.get(email=email).socialaccount_set.first()
        messages.error(request, "이메일로 가입된 계정입니다. 이메일 주소와 비밀번호를 입력해 주세요.")
        raise ImmediateHttpResponse(redirect('/accounts/login'))
