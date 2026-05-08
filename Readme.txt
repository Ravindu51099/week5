# Money Exchange Application using SQLite3

## Project Description

This project is a simple money exchange application developed using Python and SQLite3.  
The database is based on the ER diagram created for the money exchange system.

The system allows users to manage customers, accounts, currencies, transactions, and currency exchange records.

## Tables Created

I created 5 tables in this database:

1. Customer
2. Account
3. Currency
4. TransactionTable
5. Exchange

## Table Justification

### 1. Customer Table

The Customer table stores personal information about each customer, such as first name, last name, email, phone number, address, and date of birth.

This table is necessary because every account must belong to a customer. It helps the system identify who owns each account.

### 2. Account Table

The Account table stores customer account details, including account number, account type, balance, and customer ID.

This table is necessary because customers can own one or more accounts. The CustomerID field connects each account to the correct customer.

### 3. Currency Table

The Currency table stores currency information such as currency code, currency name, symbol, country, and exchange rate.

This table is necessary because the money exchange system needs to know which currencies are available and what exchange rate should be used.

### 4. TransactionTable

The TransactionTable stores deposit and withdrawal records. It includes transaction date, amount, transaction type, status, account ID, and currency code.

This table is necessary because every account transaction must be recorded for tracking and history purposes.

### 5. Exchange Table

The Exchange table stores currency exchange records. It includes the exchange date, amount from, amount to, rate used, from currency, and to currency.

This table is necessary because the main purpose of the application is to exchange money from one currency to another and keep a record of each exchange.

## Relationships

- One Customer can own many Accounts.
- One Account can have many Transactions.
- One Currency can be used in many Transactions.
- One Currency can be used as a FromCurrency in many Exchange records.
- One Currency can be used as a ToCurrency in many Exchange records.

## Technologies Used

- Python
- SQLite3
- Visual Studio Code
- GitHub

## How to Run the Project

1. Open the project folder in VS Code.
2. Open the terminal.
3. Run the following command:

```bash
python main.py