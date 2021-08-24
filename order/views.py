import requests
import json

from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import MyOrderSerializer, OrderSerializer, PaymentAuthorizationSerializer


# 카카오페이 결제 API 연동 - 결제 준비 단계
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticated,])
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    payment_method = 'kakaoPay'

    if serializer.is_valid():
        item_name = [item.get('product') for item in serializer.validated_data['items']][0]
        quantity = sum(item.get('quantity') for item in serializer.validated_data['items'])
        total_amount = sum(item.get('quantity') * item.get('price') for item in serializer.validated_data['items'])

        url = "https://kapi.kakao.com"
        headers = {
            'Authorization': "KakaoAK " + settings.KAKAO_ADMIN_KEY,
        }
        params = {
            'cid': "TC0ONETIME", # 가맹점 코드(테스트용)TC0ONETIME
            'partner_order_id': 'partner_order_id', # 가맹점 주문번호
            'partner_user_id': 'partner_user_id', # 가맹점 회원 id
            'item_name': item_name, # 상품명
            'quantity': quantity,
            'total_amount': total_amount,
            'tax_free_amount': 0,
            'approval_url': 'http://127.0.0.1:8080/cart/confirm',
            'fail_url': 'http://127.0.0.1:8080',
            'cancel_url': 'http://127.0.0.1:8080',
        }

        try:
            response = requests.post(url+"/v1/payment/ready", params=params, headers=headers)
            response = json.loads(response.text)
            payment_unique_numbers = response['tid']

            serializer.save(user=request.user, paid_amount=total_amount, payment_method=payment_method, payment_unique_numbers=payment_unique_numbers)

            return Response(response)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카카오페이 결제 API 연동 - 결제 승인 단계
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticated,])
def confirm(request):
    serializer = PaymentAuthorizationSerializer(data=request.data)
    tid_queryset = Order.objects.filter(user=request.user).values_list('payment_unique_numbers', flat=True).order_by('-created_at')
    tid = tid_queryset[0] # 가장 최근에 추가된 tid
    pg_token = request.data['pg_token']

    if serializer.is_valid():
        url = "https://kapi.kakao.com"
        headers = {
            'Authorization': "KakaoAK " + settings.KAKAO_ADMIN_KEY,
        }
        params = {
            'cid': "TC0ONETIME", # 가맹점 코드(테스트용)TC0ONETIME
            'tid': tid, # 결제 고유번호
            'partner_order_id': 'partner_order_id', # 가맹점 주문번호
            'partner_user_id': 'partner_user_id', # 가맹점 회원 id
            'pg_token': pg_token,
        }

        try:
            response = requests.post(url+"/v1/payment/approve", params=params, headers=headers)
            response = json.loads(response.text)
            payment_status = True

            print(response)

            serializer.save(user=request.user, payment_status=payment_status) # 결제 상세 내용 저장하는 model, serializer도 만들어 보기

            return Response(response)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)