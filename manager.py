from database import create_connection
from datetime import datetime

def add_customer():
    conn = create_connection()
    cursor = conn.cursor()

    first = input("First name: ")
    last = input("Last name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    dob = input("Date of birth (YYYY-MM-DD): ")

    try:
        cursor.execute("""
        INSERT INTO Customer 
        (FirstName, LastName, Email, Phone, Address, DateOfBirth)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (first, last, email, phone, address, dob))

        conn.commit()
        print("Customer added successfully.")

    except Exception as e:
        print("Error:", e)

    conn.close()


def view_customers():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()

    print("\n--- Customers ---")
    for row in rows:
        print(row)

    conn.close()


def add_account():
    conn = create_connection()
    cursor = conn.cursor()

    account_number = input("Account number: ")
    account_type = input("Account type (Savings/Current): ")
    balance = float(input("Opening balance: "))
    customer_id = int(input("Customer ID: "))

    try:
        cursor.execute("""
        INSERT INTO Account 
        (AccountNumber, AccountType, Balance, CustomerID)
        VALUES (?, ?, ?, ?)
        """, (account_number, account_type, balance, customer_id))

        conn.commit()
        print("Account created successfully.")

    except Exception as e:
        print("Error:", e)

    conn.close()


def view_accounts():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        Account.AccountID,
        Account.AccountNumber,
        Account.AccountType,
        Account.Balance,
        Customer.FirstName || ' ' || Customer.LastName AS CustomerName
    FROM Account
    INNER JOIN Customer ON Account.CustomerID = Customer.CustomerID
    """)

    rows = cursor.fetchall()

    print("\n--- Accounts ---")
    for row in rows:
        print(row)

    conn.close()


def add_currency():
    conn = create_connection()
    cursor = conn.cursor()

    code = input("Currency code (USD/LKR/NZD): ").upper()
    name = input("Currency name: ")
    symbol = input("Symbol: ")
    country = input("Country: ")
    rate = float(input("Exchange rate: "))

    try:
        cursor.execute("""
        INSERT INTO Currency
        (CurrencyCode, CurrencyName, Symbol, Country, ExchangeRate)
        VALUES (?, ?, ?, ?, ?)
        """, (code, name, symbol, country, rate))

        conn.commit()
        print("Currency added successfully.")

    except Exception as e:
        print("Error:", e)

    conn.close()
    

def update_currency_rate():
    conn = create_connection()
    cursor = conn.cursor()

    code = input("Enter Currency Code to update: ").upper()
    new_rate = float(input("Enter new exchange rate: "))

    cursor.execute("""
    UPDATE Currency
    SET ExchangeRate = ?
    WHERE CurrencyCode = ?
    """, (new_rate, code))

    conn.commit()
    conn.close()

    print("Exchange rate updated successfully.")


def view_currencies():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Currency")
    rows = cursor.fetchall()

    print("\n--- Currencies ---")
    for row in rows:
        print(row)

    conn.close()


def deposit_money():
    conn = create_connection()
    cursor = conn.cursor()

    account_id = int(input("Account ID: "))
    amount = float(input("Deposit amount: "))
    currency = input("Currency code: ").upper()

    try:
        cursor.execute("""
        UPDATE Account
        SET Balance = Balance + ?
        WHERE AccountID = ?
        """, (amount, account_id))

        cursor.execute("""
        INSERT INTO TransactionTable
        (TransactionDate, Amount, TransactionType, Status, AccountID, CurrencyCode)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), amount, "Deposit", "Completed", account_id, currency))

        conn.commit()
        print("Deposit successful.")

    except Exception as e:
        print("Error:", e)

    conn.close()


def withdraw_money():
    conn = create_connection()
    cursor = conn.cursor()

    account_id = int(input("Account ID: "))
    amount = float(input("Withdraw amount: "))
    currency = input("Currency code: ").upper()

    cursor.execute("SELECT Balance FROM Account WHERE AccountID = ?", (account_id,))
    account = cursor.fetchone()

    if account is None:
        print("Account not found.")
        conn.close()
        return

    if account[0] < amount:
        print("Insufficient balance.")
        conn.close()
        return

    try:
        cursor.execute("""
        UPDATE Account
        SET Balance = Balance - ?
        WHERE AccountID = ?
        """, (amount, account_id))

        cursor.execute("""
        INSERT INTO TransactionTable
        (TransactionDate, Amount, TransactionType, Status, AccountID, CurrencyCode)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), amount, "Withdrawal", "Completed", account_id, currency))

        conn.commit()
        print("Withdrawal successful.")

    except Exception as e:
        print("Error:", e)

    conn.close()


def view_transactions():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        TransactionTable.TransactionID,
        TransactionTable.TransactionDate,
        TransactionTable.Amount,
        TransactionTable.TransactionType,
        TransactionTable.Status,
        Account.AccountNumber,
        TransactionTable.CurrencyCode
    FROM TransactionTable
    INNER JOIN Account ON TransactionTable.AccountID = Account.AccountID
    ORDER BY TransactionTable.TransactionDate DESC
    """)

    rows = cursor.fetchall()

    print("\n--- Transactions ---")
    for row in rows:
        print(row)

    conn.close()


def exchange_currency():
    conn = create_connection()
    cursor = conn.cursor()

    from_currency = input("From currency code: ").upper()
    to_currency = input("To currency code: ").upper()
    amount_from = float(input("Amount to exchange: "))

    cursor.execute("SELECT ExchangeRate FROM Currency WHERE CurrencyCode = ?", (from_currency,))
    from_rate = cursor.fetchone()

    cursor.execute("SELECT ExchangeRate FROM Currency WHERE CurrencyCode = ?", (to_currency,))
    to_rate = cursor.fetchone()

    if from_rate is None or to_rate is None:
        print("Invalid currency code.")
        conn.close()
        return

    rate_used = to_rate[0] / from_rate[0]
    amount_to = amount_from * rate_used

    cursor.execute("""
    INSERT INTO Exchange
    (ExchangeDate, AmountFrom, AmountTo, RateUsed, FromCurrency, ToCurrency)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        amount_from,
        amount_to,
        rate_used,
        from_currency,
        to_currency
    ))

    conn.commit()
    conn.close()

    print(f"Exchange completed. You receive {amount_to:.2f} {to_currency}")


def view_exchanges():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Exchange")
    rows = cursor.fetchall()

    print("\n--- Exchange Records ---")
    for row in rows:
        print(row)

    conn.close()