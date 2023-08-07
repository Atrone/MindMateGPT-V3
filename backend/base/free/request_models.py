from pydantic import BaseModel


class GPTBody(BaseModel):
    message: str
