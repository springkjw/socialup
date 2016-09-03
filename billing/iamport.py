#-*- coding: utf-8 -*-
import urllib2
import json

from django.conf import settings


def get_access_token():
    access_data = {
        'imp_key': settings.IAMPORT_KEY,
        'imp_secret': settings.IAMPORT_SECRET
    }
    url = "https://api.iamport.kr/users/getToken"
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    access_res = json.loads(urllib2.urlopen(req, json.dumps(access_data)).read())

    if access_res['code'] is 0:
        return access_res['response']['access_token']
    else:
        return None


def validation_prepare(merchant_id, amount, *args, **kwargs):
    access_token = get_access_token()

    if access_token:
        access_data = {
            'merchant_uid': merchant_id,
            'amount': amount
        }

        url = "https://api.iamport.kr/payments/prepare?_token=" + access_token

        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')

        res = json.loads(urllib2.urlopen(req, json.dumps(access_data)).read())

        if res['code'] is not 0:
            raise ValueError("API 연결에 문제가 생겼습니다.")
    else:
        raise ValueError("인증 토큰이 없습니다.")


def get_transaction(merchant_id, *args, **kwargs):
    access_token = get_access_token()

    # print access_token
    if access_token:
        url = "https://api.iamport.kr/payments/find/" + merchant_id + '?_token=' + access_token
        res = json.loads(urllib2.urlopen(url).read())

        if res['code'] is 0:
            context = {
                'imp_id' : res['response']['imp_uid'],
                'merchant_id' : res['response']['merchant_uid'],
                'amount' : res['response']['amount'],
                'status' : res['response']['status'],
                'type' : res['response']['pay_method'],
                'receipt_url' : res['response']['receipt_url']
            }
            return context
        else:
            return None
    else:
        raise ValueError("인증 토큰이 없습니다.")
