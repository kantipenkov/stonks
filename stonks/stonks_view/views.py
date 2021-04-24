from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from stonks_view.serializers import UserSerializer, CompanySerializer, CopmanyEarningsSerializer
from django.contrib.auth.models import User
from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CopmanyEarnings

# Create your views here.

# def index(request):
#     return render(request, 'stonks_view/index.html')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True)
    def earnings(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CopmanyEarnings.objects.filter(copmany=company.ticker)
        serializer = CopmanyEarningsSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

class CopmanyEarningsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CopmanyEarnings.objects.all()
    serializer_class = CopmanyEarningsSerializer
    # def list(self, request):
    #     queryset = CopmanyEarnings.objects.all()
    #     serializer = CopmanyEarningsSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = CopmanyEarnings.objects.filter(copmany=pk)
    #     serializer = CopmanyEarningsSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)





# class CopmanyEarningsView(APIView):

#     def get(self, request, ticker):
#         return self.get_serialized(request, ticker)

#     def get_serialized(self,request, ticker):
#         # queryset = CopmanyEarnings.objects.filter(copmany=ticker)
#         serializer = CopmanyEarningsSerializer(CopmanyEarnings.objects.filter(copmany=ticker), many=True, context={'request':request})
#         return Response(serializer.data)