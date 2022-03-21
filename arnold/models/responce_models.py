from pydantic import BaseModel, Field


class WorkflowResponce(BaseModel):
    id: str = Field(..., alias="_id")
    step_types: list[str]
