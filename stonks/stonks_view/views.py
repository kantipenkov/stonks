from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from stonks_view.serializers import UserSerializer, CompanySerializer, CompanyEarningsSerializer, CompanyBalanceSerializer, CompanyCashFlowSerilaizer, WatchListSerializer, UserRegistrationSerializer, WatchItemSerializer
from django.contrib.auth.models import User
from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CompanyEarnings, WatchList, WatchItem

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True)
    def earnings(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyEarnings.objects.filter(company=company.ticker)
        serializer = CompanyEarningsSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    @action(detail=True)
    def balance(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyBalance.objects.filter(company=company.ticker)
        serializer = CompanyBalanceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def cash_flow(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyCashFlow.objects.filter(company=company.ticker)
        serializer = CompanyCashFlowSerilaizer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class CompanyEarningsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyEarnings.objects.all()
    serializer_class = CompanyEarningsSerializer
    # def list(self, request):
    #     queryset = CompanyEarnings.objects.all()
    #     serializer = CompanyEarningsSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = CompanyEarnings.objects.filter(copmany=pk)
    #     serializer = CompanyEarningsSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

class CompanyBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyBalance.objects.all()
    serializer_class = CompanyBalanceSerializer

class CompanyCashFlowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyCashFlow.objects.all()
    serializer_class = CompanyCashFlowSerilaizer

class WatchListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def items(self, request, *args, **kwargs):
        queryset =  WatchItem.objects.filter(watch_list=self.get_object())
        serializer = WatchItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WatchItemsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WatchItem.objects.all()
    serializer_class = WatchItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

