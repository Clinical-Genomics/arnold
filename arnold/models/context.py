from pydantic import BaseModel


class APIContextObject(BaseModel):
    host: str
    port: int
