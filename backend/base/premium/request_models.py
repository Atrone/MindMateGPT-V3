from pydantic import BaseModel


class InsightBody(BaseModel):
    recipient: str


class AnalysisBody(BaseModel):
    recipient: str
    journals: str
