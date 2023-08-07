from pydantic import BaseModel


class InsightBody(BaseModel):
    recipient: str
