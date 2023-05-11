Charting Service
================

The Charting and analytics Service is Django based web application that provides API endpoints for charting and 
analytics purpose.It allows user to retrive balance breakdowns ,income and expenses data and transaction information for the Companies.


## Features

- `getAccountBalanceBreakdown`: Retrieves the balance breakdown across accounts of a company, with monthly increments.
- `getIncomeExpenseForDate`: Retrieves the income and expense of a company for a given month/year.
- `getTransactionsForInterval`: Retrieves all the transactions between a start and end datetime for a given company.

## Prerequisites

Before running the Charting and Analytics Service, ensure you have the following prerequisites installed:

- Python 3.x
- Django
- SQLite

## Installation

1. Clone the repository:

#    Create a virtual environment:

``` https://github.com/ThakurPushpendra/QuickBook.git

python3 -m venv venv

 #   Activate the virtual environment:

source venv/bin/activate

#  Install the dependencies:

pip install -r requirements.txt

API Documentation:
==================
getAccountBalanceBreakdown

Retrieves the balance breakdown across accounts of a company, with monthly increments.

    Endpoint: /api/getAccountBalanceBreakdown/<companyId>/
    HTTP Method: GET
    Parameters:
        companyId: ID of the company for which the data is requested (integer)
    Response Format:
        3D array of [datetime, [[account_name and balance]]]


getIncomeExpenseForDate:
========================

Retrieves the income and expense of a company for a given month/year.

    Endpoint: /api/getIncomeExpenseForDate/<companyId>/<year>/<month>/
    HTTP Method: GET
    Parameters:
        companyId: ID of the company for which the data is requested (integer)
        year: Year of the data (integer)
        month: Month of the data (integer)
    Response Format:
        JSON object with income and expense properties


getTransactionsForInterval:
===========================

Retrieves all the transactions between a start and end datetime for a given company.

    Endpoint: /api/getTransactionsForInterval/<companyId>/<start_datetime>/<end_datetime>/
    HTTP Method: GET
    Parameters: