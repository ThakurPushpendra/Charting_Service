# api/serializers.py
from rest_framework import serializers
from .models import Company, Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    from_account = AccountSerializer(read_only=True)
    to_account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class CompanyBalanceSerializer(serializers.ModelSerializer):
    account_balances = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'account_balances']

    def get_account_balances(self, obj):
        # Get a list of all accounts for this company
        accounts = Account.objects.filter(company=obj)

        # Initialize a dictionary to hold the balance breakdown for each month
        balances_by_month = {}

        # Iterate over each account
        for account in accounts:
            # Get a list of transactions for this account
            transactions = Transaction.objects.filter(account=account)

            # Iterate over each transaction
            for transaction in transactions:
                # Get the month and year of the transaction
                year = transaction.date.year
                month = transaction.date.month

                # Initialize the balance for this month, if necessary
                if (year, month) not in balances_by_month:
                    balances_by_month[(year, month)] = {}

                # Add the transaction amount to the balance for this month
                balances_by_month[(year, month)][account.name] = balances_by_month[(year, month)].get(account.name, 0) + transaction.amount

        # Convert the balances by month dictionary to the expected output format
        result = []
        for (year, month), balances in balances_by_month.items():
            result.append([
                f"{year}-{month:02d}-01",
                [[account_name, balance] for account_name, balance in balances.items() if balance != 0]
            ])

        return result


class IncomeExpenseSerializer(serializers.ModelSerializer):
    income = serializers.SerializerMethodField()
    expense = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'income', 'expense']

    def get_income(self, obj):
        # Calculate the total income for the specified month/year
        # Implement the logic to calculate the total income based on the Transaction model and the input parameters
        # Return the total income as a float
        pass

    def get_expense(self, obj):
        # Calculate the total expense for the specified month/year
        # Implement the logic to calculate the total expense based on the Transaction model and the input parameters
        # Return the total expense as a float
        pass
