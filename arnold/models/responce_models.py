from pydantic import BaseModel


class WorkflowResponce(BaseModel):
    _id: str
    step_types: list[str]
