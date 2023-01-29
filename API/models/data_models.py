from __future__ import annotations

from pydantic import BaseModel, Required, Field


PASSWORD_PARAMS = {"min_length": 8, "max_length": 255, "exclude": True}

#
class Account(BaseModel):
    account_number: int  # same as db id, not directly accessible
    balance: int | float = Field(
        ge=0, default=0, description="The balance must be greater than or equal to zero"
    )


class Customer(BaseModel):
    name: str = Field(default=Required, description="Name of the customer")


class CustomerIn(Customer):
    # TODO Use regex to validate password
    password: str = Field(
        default=Required, description="Password of the customer", **PASSWORD_PARAMS
    )


class CustomerInDB(CustomerIn):
    accounts: list[Account] = Field(default=[], exclude=True)  # not directly accessible


class CustomerOutDB(Customer):
    hashed_password: str
    accounts_id: int


class Bank(BaseModel):
    customers: list[CustomerIn] = []  # not directly accessible, will be handled by the DB


class BankDB(Bank):
    current_user: Customer | None


