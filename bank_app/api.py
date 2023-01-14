from typing import Union

from fastapi import FastAPI
from bank import Bank

app = FastAPI()

bank = Bank()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/")
def get_bank():
    return bank.to_json()


@app.get("/customers")
def get_customers():
    return [customer.to_json() for customer in bank.customers]


@app.get("/user")
def get_logged_in_user():
    return bank.current_user.to_json() if bank.current_user else None


@app.put("/add/{name}")
def add_customer(name: str, password: str):
    if bank.add_customer(name, password):
        return bank.get_customer(name).to_json()


@app.get("/{name}")
def get_customer(name: str):
    if customer := bank.get_customer(name):
        return customer.to_json()


@app.put("/customers/{name}/change_password")
def change_password(name: str, new_password: str):
    if bank.change_customer_password(name, new_password):
        return bank.get_customer(name).to_json()


@app.put("/customers/{name}/remove")
def remove_customer(name):
    if customer := bank.get_customer(name):
        bank.remove_customer(name)
        return customer.to_json()


@app.put("/login")
def login(name: str, password: str):
    if bank.login(name, password):
        return bank.current_user.to_json()


@app.get("bank/logout")
def logout():
    if customer := bank.current_user:
        if bank.logout():
            return customer.to_json()


@app.get("/bank/accounts")
def get_accounts():
    if accounts := bank.get_accounts():
        return [account.to_json() for account in accounts]


@app.put("/bank/add/{account_number}")
def add_account(account_number: int):
    if bank.add_account(account_number):
        return bank.get_account(account_number).to_json()


@app.put("/bank/remove/{account_number}")
def remove_account(account_number: int):
    if account := bank.get_account(account_number):
        if bank.remove_account(account_number):
            return account.to_json()


@app.get("/bank/account/{account_number}")
def get_account(account_number: int):
    if account := bank.get_account(account_number):
        return account.to_json()


@app.put("/bank/{account_number}/deposit/{amount}")
def deposit(account_number: int, amount: Union[int, float]):
    if bank.deposit(account_number, amount):
        return bank.get_account(account_number).to_json()


@app.put("/bank/{account_number}/withdraw/{amount}")
def withdraw(account_number: int, amount: Union[int, float]):
    if bank.withdraw(account_number, amount):
        return bank.get_account(account_number).to_json()
