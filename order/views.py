from django.shortcuts import render

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import MyOrderSerializer


class OrdersList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)