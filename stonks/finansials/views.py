from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from finansials.serializers import CompanySerializer, CompanyIncomeReportSerializer, CompanyBalanceReportSerializer
# from finansials.serializers import UserSerializer, CompanySerializer, CompanyEarningsSerializer, UserRegistrationSerializer
# from django.contrib.auth.models import User
from finansials.models import Company, CompanyIncomeReport, CompanyBalanceReport
# from stonks.finansials.models import CompanyBalanceReport

# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True)
    def income_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyIncomeReport.objects.filter(company=company)
        serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    @action(detail=True)
    def balance_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyBalanceReport.objects.filter(company=company.ticker)
        serializer = CompanyBalanceReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # @action(detail=True)
    # def cash_flow(self, request, *args, **kwargs):
    #     company = self.get_object()
    #     queryset = CompanyCashFlow.objects.filter(company=company.ticker)
    #     serializer = CompanyCashFlowSerilaizer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

class CompanyIncomeReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyIncomeReport.objects.all()
    serializer_class = CompanyIncomeReportSerializer

    # def list(self, request):
    #     queryset = CompanyIncomeReport.objects.all()
    #     serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

    def retrieve(self, request:Request, pk=None):
        try:
            int(pk)
            queryset = CompanyIncomeReport.objects.all()
            income_report = get_object_or_404(queryset, pk=pk)
            serializer = CompanyIncomeReportSerializer(income_report, context={'request': request})
        except ValueError as e:
            queryset = CompanyIncomeReport.objects.filter()
            serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class CompanyBalanceReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyBalanceReport.objects.all()
    serializer_class = CompanyBalanceReportSerializer

    def retrieve(self, request: Request, pk=None):
        try:
            int(pk)
            queryset = CompanyBalanceReport.objects.all()
            income_report = get_object_or_404(queryset, pk=pk)
            serializer = CompanyBalanceReportSerializer(income_report, context={'request': request})
        except ValueError as e:
            queryset = CompanyBalanceReport.objects.filter()
            serializer = CompanyBalanceReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# class CompanyBalanceViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = CompanyBalance.objects.all()
#     serializer_class = CompanyBalanceSerializer

# class CompanyCashFlowViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = CompanyCashFlow.objects.all()
#     serializer_class = CompanyCashFlowSerilaizer

# class WatchListViewSet(viewsets.ModelViewSet):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#     permission_classes=[permissions.IsAuthenticatedOrReadOnly]

#     @action(detail=True)
#     def items(self, request, *args, **kwargs):
#         queryset =  WatchItem.objects.filter(watch_list=self.get_object())
#         serializer = WatchItemSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     @action(detail=True)
#     def compare(self, request, *args, **kwargs):
#         # import itertools
#         watch_list = self.get_object()
#         watch_companies = WatchItem.objects.filter(watch_list=watch_list).values("company")
#         earnings_queryset = CompanyEarnings.objects.filter(company__in=watch_companies).order_by("company")
#         balance_queryset = CompanyBalance.objects.filter(company__in=watch_companies).order_by("company")
#         cash_flow_queryset = CompanyCashFlow.objects.filter(company__in=watch_companies).order_by("company")

#         earnings_serializer = CompanyEarningsSerializer(earnings_queryset, many=True, context={'request': request})
#         balance_serializer = CompanyBalanceSerializer(balance_queryset, many=True, context={'request': request})
#         cash_flow_serializer = CompanyCashFlowSerilaizer(cash_flow_queryset, many=True, context={'request': request})
#         serilaizer_list = (earnings_serializer.data, balance_serializer.data, cash_flow_serializer.data)
#         return Response(data=serilaizer_list)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class WatchItemsViewSet(viewsets.ModelViewSet):
#     queryset = WatchItem.objects.all()
#     serializer_class = WatchItemSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

