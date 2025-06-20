from __future__ import annotations

import datetime
from ofxstatement.statement import Currency
from decimal import Decimal
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


class Amount(BaseModel):
    amount: Decimal
    currency: Currency

    class Config:
        arbitrary_types_allowed = True

    @field_validator("currency", mode="before")
    def validate_currency(cls, value):
        if isinstance(value, str):
            return Currency(value)
        return value


class Account(BaseModel):
    bban: Optional[str] = None


class ReportExchangeRate(BaseModel):
    sourceCurrency: Optional[Currency] = None
    targetCurrency: Optional[Currency] = None
    unitCurrency: Optional[Currency] = None
    exchangeRate: Optional[float] = None
    quotationDate: Optional[datetime.date] = None

    @field_validator("sourceCurrency", "targetCurrency", "unitCurrency", mode="before")
    def validate_currency(cls, value):
        if isinstance(value, str):
            return Currency(value)
        return value

    class Config:
        arbitrary_types_allowed = True


class CurrencyExchangeAmex(BaseModel):
    """
    Context: Issue #11

    Temporary Fix:
    This addresses the lack of normalization of American Express data to the GoCardless specification.

    Note: This class should be removed once the normalization process is completed.
    """

    sourceCurrency: Optional[Currency] = None
    targetCurrency: Optional[Currency] = None
    unitCurrency: Optional[Currency] = None
    exchangeRate: Optional[float] = None
    instructedAmount: Optional[Amount] = None

    @field_validator("sourceCurrency", "targetCurrency", "unitCurrency", mode="before")
    def validate_currency(cls, value):
        if isinstance(value, str):
            return Currency(value)
        return value

    class Config:
        arbitrary_types_allowed = True


class NordigenTransactionModel(BaseModel):
    """
    Nordigen data transaction model.
    """

    balanceAfterTransaction: Optional[float] = None
    bankTransactionCode: Optional[str] = None
    bookingDate: Optional[datetime.date] = None
    bookingDateTime: Optional[datetime.datetime] = None
    checkId: Optional[str] = None
    creditorAccount: Optional[Account] = None
    creditorAgent: Optional[str] = None
    creditorId: Optional[str] = None
    creditorName: Optional[str] = None
    currencyExchange: Optional[List[ReportExchangeRate] | CurrencyExchangeAmex] = None
    debtorAccount: Optional[Account] = None
    debtorAgent: Optional[str] = None
    debtorName: Optional[str] = None
    endToEndId: Optional[str] = None
    entryReference: Optional[str] = None
    internalTransactionId: Optional[str] = None
    mandateId: Optional[str] = None
    merchantCategoryCode: Optional[str] = None
    proprietaryBankTransactionCode: Optional[str] = None
    purposeCode: Optional[str] = None
    remittanceInformationStructured: Optional[str] = None
    remittanceInformationStructuredArray: Optional[List[str]] = None
    remittanceInformationUnstructured: Optional[str] = None
    remittanceInformationUnstructuredArray: Optional[List[str]] = None
    transactionAmount: Amount
    transactionId: Optional[str] = None
    ultimateCreditor: Optional[str] = None
    ultimateDebtor: Optional[str] = None
    valueDate: Optional[datetime.date] = None
    valueDateTime: Optional[datetime.datetime] = None
