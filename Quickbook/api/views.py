from django.shortcuts import render
# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from .models import Company, Account, Transaction
from .serializers import AccountSerializer
from .serializers import IncomeExpenseSerializer
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from datetime import date
from django.utils.timezone import make_aware
    


#Endpoint 1: getAccountBalanceBreakdown

@api_view(['GET'])
def getAccountBalanceBreakdown(request, companyId):
    company = get_object_or_404(Company, id=companyId)
    accounts = Account.objects.filter(company=company)
    transactions = Transaction.objects.filter(
        account__in=accounts,
        date__isnull=False
    ).annotate(
        month=TruncMonth('date')
    ).values(
        'month',    
        'account__name'
    ).annotate(
        balance=Sum('amount')
    )
    serializer = AccountSerializer(transactions, many=True)
    return Response(serializer.data)


#    Endpoint 2: getIncomeExpenseForDate


def getIncomeExpenseForDate(request, companyId, month, year):
    company = get_object_or_404(Company, id=companyId)
    start_date = make_aware(date(year, month, 1))
    end_date = make_aware(date(year, month, 1)).replace(day=31)
    transactions = Transaction.objects.filter(
        account__company=company,
        date__range=[start_date, end_date]
    )
    income = transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    expense = transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    serializer = IncomeExpenseSerializer({'income': income, 'expense': expense})
    return Response(serializer.data)


#  Endpoint 3: getTransactionsForInterval

@api_view(['GET'])
def getTransactionsForInterval(request, companyId, start_datetime, end_datetime):
    company = Company.objects.get(id=companyId)
    transactions = Transaction.objects.filter(
        account__company=company,
        date__range=[start_datetime, end_datetime]
    )
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
