from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from finansials.serializers import CompanySerializer, CompanyIncomeReportSerializer, CompanyBalanceReportSerializer, CompanyCashFlowReportSerializer

# from django.contrib.auth.models import User
from finansials.models import Company, CompanyIncomeReport, CompanyBalanceReport, CompanyCashFlowReport, ReportType
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
    def income_annual_reports(self, request, pk=None):
        company = self.get_object()
        queryset = CompanyIncomeReport.objects.filter(company=company).filter(report_type=ReportType.Annual)
        serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    @action(detail=True)
    def income_quarterly_reports(self, request, pk=None):
        company = self.get_object()
        queryset = CompanyIncomeReport.objects.filter(company=company).filter(report_type=ReportType.Quarterly)
        serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    @action(detail=True)
    def balance_annual_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyBalanceReport.objects.filter(company=company.ticker).filter(report_type=ReportType.Annual)
        serializer = CompanyBalanceReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def balance_quarterly_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyBalanceReport.objects.filter(company=company.ticker).filter(report_type=ReportType.Quarterly)
        serializer = CompanyBalanceReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def cash_flow_annual_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyCashFlowReport.objects.filter(company=company.ticker).filter(report_type=ReportType.Annual)
        serializer = CompanyCashFlowReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    @action(detail=True)
    def cash_flow_quarterly_reports(self, request, *args, **kwargs):
        company = self.get_object()
        queryset = CompanyCashFlowReport.objects.filter(company=company.ticker).filter(report_type=ReportType.Quarterly)
        serializer = CompanyCashFlowReportSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CompanyIncomeReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyIncomeReport.objects.all()
    serializer_class = CompanyIncomeReportSerializer

    # def list(self, request):
    #     queryset = CompanyIncomeReport.objects.all()
    #     serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)

    # def retrieve(self, request:Request, pk=None, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     try:
    #         int(pk)
    #         queryset = CompanyIncomeReport.objects.all()
    #         income_report = get_object_or_404(queryset, pk=pk)
    #         serializer = CompanyIncomeReportSerializer(income_report, context={'request': request})
    #     except ValueError as e:
    #         queryset = CompanyIncomeReport.objects.filter()
    #         serializer = CompanyIncomeReportSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

class CompanyBalanceReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyBalanceReport.objects.all()
    serializer_class = CompanyBalanceReportSerializer

    # def retrieve(self, request: Request, pk=None):
    #     try:
    #         int(pk)
    #         queryset = CompanyBalanceReport.objects.all()
    #         income_report = get_object_or_404(queryset, pk=pk)
    #         serializer = CompanyBalanceReportSerializer(income_report, context={'request': request})
    #     except ValueError as e:
    #         queryset = CompanyBalanceReport.objects.filter()
    #         serializer = CompanyBalanceReportSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

class CompanyCashFlowReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyCashFlowReport.objects.all()
    serializer_class = CompanyCashFlowReportSerializer

    # def retrieve(self, request: Request, pk=None):
    #     try:
    #         int(pk)
    #         queryset = CompanyCashFlowReport.objects.all()
    #         income_report = get_object_or_404(queryset, pk=pk)
    #         serializer = CompanyCashFlowReportSerializer(income_report, context={'request': request})
    #     except ValueError as e:
    #         queryset = CompanyCashFlowReport.objects.filter()
    #         serializer = CompanyCashFlowReportSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
