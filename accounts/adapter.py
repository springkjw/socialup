# -*- coding: utf-8 -*-
from django import forms
from allauth.account.adapter import (
    app_settings,
    DefaultAccountAdapter,
)


class AccountAdapter(DefaultAccountAdapter):
    # login 후 redirect 페이지
    def get_login_redirect_url(self, request):
        return '/'

    def clean_password(self, password):
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if len(password) < min_length:
            if len(password) < min_length:
                error_message = "비밀번호는 %s자리 이상이여야합니다." % (min_length)
                raise forms.ValidationError(error_message)
            return password
