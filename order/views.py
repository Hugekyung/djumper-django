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
from .serializers import MyOrderSerializer, OrderSerializer


# 카카오페이 결제 API 연동 - 결제 준비 단계
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticated,])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        item_name = [item.get('product') for item in serializer.validated_data['items']][0]
        quantity = sum(item.get('quantity') for item in serializer.validated_data['items'])
        total_amount = sum(item.get('quantity') * item.get('price') for item in serializer.validated_data['items'])

        url = "https://kapi.kakao.com"
        headers = {
            'Authorization': "KakaoAK " + settings.KAKAO_ADMIN_KEY,
            # 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        params = {
            'cid': "TC0ONETIME", # 가맹점 코드(테스트용)TC0ONETIME
            'partner_order_id': 'partner_order_id', # 가맹점 주문번호
            'partner_user_id': 'partner_user_id', # 가맹점 회원 id
            'item_name': item_name, # 상품명
            'quantity': quantity,
            'total_amount': total_amount,
            'tax_free_amount': 0,
            'approval_url': 'http://127.0.0.1:8080/cart/success',
            'fail_url': 'http://127.0.0.1:8080',
            'cancel_url': 'http://127.0.0.1:8080',
        }

        try:
            response = requests.post(url+"/v1/payment/ready", params=params, headers=headers)
            response = json.loads(response.text)

            serializer.save(user=request.user, paid_amount=total_amount)
            
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