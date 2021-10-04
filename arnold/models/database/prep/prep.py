from typing import Optional
from pydantic import Field, validator
from arnold.models.database.prep.microbial_prep import MicrobialPrep
from arnold.models.database.prep.sars_cov_2_prep import SarsCov2Prep


class Prep(MicrobialPrep, SarsCov2Prep):
    """LIMS Prep Collection"""

    prep_id: str
    id: Optional[str] = Field(..., alias="_id")
    sample_id: str
    workflow: str

    @validator("id", always=True)
    def set_id(cls, v, values: dict) -> str:
        """sett _id to prep_id"""

        return values.get("prep_id")

    class Config:
        allow_population_by_field_name = True
