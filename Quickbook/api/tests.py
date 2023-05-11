from django.test import TestCase
from django.urls import reverse
from .models import Account,Company,Transaction
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .serializers import AccountSerializer
from django.utils.timezone import make_aware

class AccountBalanceBreakdownTest(TestCase):
    def setUp(self):
        #  Set up any initial data required for the test
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.company = Company.objects.create(name='Test Company')
        self.account = Account.objects.create(name='Test Account', company=self.company)
        self.transaction = Transaction.objects.create(account=self.account,amount = 100)


    def test_get_account_balance_breakdown(self):
        # Build the URL for the API endpoint
        url = reverse('get-account-balance-breakdown', args=[self.company.id])
        # Authenticate the client if necessary
        self.client.force_authenticate(user=self.user)
        # Send a GET request to the API endpoint
        response = self.client.get(url)
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data matches the expected serialized data
        expected_data = [
            {
                'month': self.transaction.date.strftime('%Y-%m'),
                'account__name': self.account.name,
                'balance': self.transaction.amount
            }
        ]
        self.assertEqual(response.data, expected_data)


class IncomeExpenseForDataTest(TestCase):
    def setUp(self):
        #  Set up any initial data required for the test
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.company = Company.objects.create(name='Test Company')
        self.account = Account.objects.create(name='Test Account', company=self.company)
        self.transaction1 = Transaction.objects.create(account=self.account,amount = 100)
        self.transaction2 = Transaction.objects.create(account=self.account, amount=-50)

    def test_get_income_expense_for_date(self):
        # Build the URL for the API endpoint
        url = reverse('get-income-expense-for-date', args=[self.company.id, 1, 2023])  # Assuming month=1 and year=2023

        # Authenticate the client if necessary
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the API endpoint
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data matches the expected serialized data
        expected_data = {
            'income': 100,
            'expense': -50
        }
        self.assertEqual(response.data, expected_data)


class TransactionForIntervalTest(TestCase):
    def setUp(self):
        # Set up any initial data required for the test
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.company = Company.objects.create(name='Test Company')
        self.account = Account.objects.create(name='Test Account', company=self.company)
    #    date__range=[(2023, 1, 1), (2023, 1, 31)]
        self.start_datetime = make_aware((2023, 1, 1))  #  start datetime
        self.end_datetime = make_aware((2023, 1, 31))  #  end datetime
        self.transaction1 = Transaction.objects.create(account=self.account, amount=100, date=self.start_datetime)
        self.transaction2 = Transaction.objects.create(account=self.account, amount=-50, date=self.end_datetime)


    def test_get_transactions_for_interval(self):
        # Build the URL for the API endpoint
        url = reverse('get-transactions-for-interval', args=[self.company.id, self.start_datetime, self.end_datetime])

        # Authenticate the client if necessary
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the API endpoint
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data matches the expected serialized data
        expected_data = [
            {
                'id': self.transaction1.id,
                'account': self.account.id,
                'amount': 100,
                'date': self.start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            },
            {
                'id': self.transaction2.id,
                'account': self.account.id,
                'amount': -50,
                'date': self.end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
        ]
        self.assertEqual(response.data, expected_data)

