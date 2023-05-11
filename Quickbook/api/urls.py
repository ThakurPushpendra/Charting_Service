from django.urls import path
from . import views

urlpatterns = [
    #  path('', views.getAccountBalanceBreakdown),
    path('getAccountBalanceBreakdown/<int:companyId>', views.getAccountBalanceBreakdown),
    # path('getIncomeExpenseForDate', views.getIncomeExpenseForDate),
    path('company/<int:companyId>/income-expense/<int:year>/<int:month>/',views.getIncomeExpenseForDate),
    # path('getTransactionsForInterval', views.getTransactionsForInterval),
    path('company/<int:companyId>/transactions/<str:start_datetime>/<str:end_datetime>/', views.getTransactionsForInterval, name='get_transactions'),
]
