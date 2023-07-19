from pydantic import BaseModel


class PaymentBody(BaseModel):
    id: str


class GPTBody(BaseModel):
    message: str


class KeyBody(BaseModel):
    key: str
