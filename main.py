from database import create_tables
from manager import (
    add_customer,
    view_customers,
    add_account,
    view_accounts,
    add_currency,
    view_currencies,
    deposit_money,
    withdraw_money,
    view_transactions,
    exchange_currency,
    view_exchanges,
    update_currency_rate
)

def menu():
    print("\n========== BANK & CURRENCY EXCHANGE SYSTEM ==========")
    print("1. Add Customer")
    print("2. View Customers")
    print("3. Add Account")
    print("4. View Accounts")
    print("5. Add Currency")
    print("6. View Currencies")
    print("7. Deposit Money")
    print("8. Withdraw Money")
    print("9. View Transactions")
    print("10. Exchange Currency")
    print("11. View Exchange Records")
    print("12. Update Currency Rate")
    print("13. Exit")

def main():
    create_tables()

    while True:
        menu()
        choice = input("Select option: ")

        if choice == "1":
            add_customer()
        elif choice == "2":
            view_customers()
        elif choice == "3":
            add_account()
        elif choice == "4":
            view_accounts()
        elif choice == "5":
            add_currency()
        elif choice == "6":
            view_currencies()
        elif choice == "7":
            deposit_money()
        elif choice == "8":
            withdraw_money()
        elif choice == "9":
            view_transactions()
        elif choice == "10":
            exchange_currency()
        elif choice == "11":
            view_exchanges()
        elif choice == "12":
            update_currency_rate()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()