import sqlite3

DB_NAME = "bank_exchange.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Phone TEXT,
        Address TEXT,
        DateOfBirth TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account (
        AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
        AccountNumber TEXT NOT NULL UNIQUE,
        AccountType TEXT NOT NULL,
        Balance REAL NOT NULL DEFAULT 0,
        CustomerID INTEGER NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Currency (
        CurrencyCode TEXT PRIMARY KEY,
        CurrencyName TEXT NOT NULL,
        Symbol TEXT,
        Country TEXT,
        ExchangeRate REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TransactionTable (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        TransactionDate TEXT NOT NULL,
        Amount REAL NOT NULL,
        TransactionType TEXT NOT NULL,
        Status TEXT NOT NULL,
        AccountID INTEGER NOT NULL,
        CurrencyCode TEXT NOT NULL,
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
        ON DELETE CASCADE,
        FOREIGN KEY (CurrencyCode) REFERENCES Currency(CurrencyCode)
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS Exchange (
    ExchangeID INTEGER PRIMARY KEY AUTOINCREMENT,
    ExchangeDate TEXT NOT NULL,
    AmountFrom REAL NOT NULL,
    AmountTo REAL NOT NULL,
    RateUsed REAL NOT NULL,
    FromCurrency TEXT NOT NULL,
    ToCurrency TEXT NOT NULL,
    TransactionID INTEGER UNIQUE,   -- THIS LINE IS IMPORTANT
    FOREIGN KEY (FromCurrency) REFERENCES Currency(CurrencyCode),
    FOREIGN KEY (ToCurrency) REFERENCES Currency(CurrencyCode),
    FOREIGN KEY (TransactionID) REFERENCES TransactionTable(TransactionID)
)
""")

    conn.commit()
    conn.close()