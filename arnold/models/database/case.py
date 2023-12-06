from pydantic import BaseModel, ConfigDict

from arnold.models.database.pipeline import Pipeline
from arnold.models.database.analysis_sample import AnalysisSample


class Case(BaseModel):
    id: str
    pipeline: Pipeline
    samples: list[AnalysisSample]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "subsonichedgehog",
                "pipeline": {"name": "MIP", "version": "0.0.0"},
                "samples": [{"id": "ACC2341", "pipeline_qc_metrics": "{}"}],
            }
        },
    )
