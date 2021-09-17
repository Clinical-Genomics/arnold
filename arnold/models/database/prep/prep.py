from typing import Optional


from pydantic import Field

from beanie import Document

from arnold.models.database.prep.microbial_prep import MicrobialPrep


class Prep(Document, MicrobialPrep):
    """LIMS Prep Collection"""

    id: Optional[str] = Field(..., alias="_id")
    prep_id: str
    sample_id: str
    workflow: str
