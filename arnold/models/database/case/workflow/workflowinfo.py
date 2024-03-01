"""This module holds the pipeline model."""
from pydantic import BaseModel


class WorkflowInfo(BaseModel):
    workflow: str
    version: str
