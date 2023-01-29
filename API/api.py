from __future__ import annotations

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import FastAPI, Path, Query, Body, Depends
from pydantic import Required

from API.models.data_models import CustomerInDB, CustomerOutDB, Bank, Customer, CustomerIn, PASSWORD_PARAMS, Account

app = FastAPI()


# UTILITY FUNCTIONS
# ------------------------------------

def hash_password(password: str) -> str:
    return bcrypt.using(rounds=13).hash(password)


def save_customer(customer: CustomerInDB):
    hashed_password = hash_password(customer.password)
    customer_out_db = CustomerOutDB(**customer.dict(), hashed_password=hashed_password)
    # TODO Save to DB



# SETUP
# -----------------------------------

bank = Bank()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


# API
# -----------------------------------

@app.post("/auth")
def authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO Do some authentication
    pass


@app.get("/customers")
def get_customers() -> list[Customer]:
    pass


@app.post("/customers/add")
def add_customer(
    customer: CustomerIn = Body(
        description="The customer to be added",
    )
) -> Customer:
    pass


@app.get("/customers/{name}")
def get_customer(name: str = Path(title="Name of the customer")) -> Customer:
    pass


@app.delete("/customers/remove")
def remove_customer(customer: CustomerIn):
    pass


@app.put("/login")
def login(customer: CustomerIn) -> Customer:
    pass


# API -> REQUIRES LOGIN
# ------------------


@app.put("/logout")
def logout() -> Customer:
    pass


@app.put("/change_password")
def change_customer_password(
    current_password: str = Query(
        default=Required, description="Current password", **PASSWORD_PARAMS
    ),
    new_password: str = Query(
        default=Required, description="New password", **PASSWORD_PARAMS
    ),
) -> Customer:
    # if logged in
    # if current password matches
    # change to new password
    pass


@app.get("/accounts")
def get_accounts() -> list[Account]:
    pass


@app.post("/accounts/add")
def add_account() -> Account:
    pass


@app.delete("/accounts/remove")
def remove_account(account_number: int = Query(default=Required, )):
    pass


@app.get("/accounts/{account_number}")
def get_account(
    account_number: int = Path(
        default=Required, description="Account number of the account", gt=0
    )
) -> Account:
    pass


@app.put("/accounts/{account_number}/deposit")
def deposit(
    account_number: int = Path(
        default=Required, description="Account number of the account", gt=0
    ),
    amount: int = Query(
        default=Required, description="Amount to be deposited to the account", gt=0
    ),
) -> Account:
    pass


@app.put("/accounts/{account_number}/withdraw")
def withdraw(
        account_number: int = Path(
            default=Required, description="Account number of the account", gt=0
        ),
        amount: int = Query(
            default=Required, description="Amount to be withdrawn from the account", gt=0
        ),
) -> Account:
    pass
