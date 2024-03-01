from pydantic import BaseModel

from arnold.models.database.case.workflow.balsamic import Balsamic


class Case(BaseModel):
    id: str
    case_info: Balsamic
