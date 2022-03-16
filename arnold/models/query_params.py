from typing import Optional, Literal

from pydantic import BaseModel


class ListQuery(BaseModel):
    page_size: Optional[int] = 5
    page_num: Optional[int] = 0
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend"
    sort_key: Optional[str] = "sample_id"
    artifact_udf: Optional[str] = None
    artifact_udf_rule: Literal["$gt", "$lt", "$eq"] = None
    artifact_udf_value: Optional[str] = None
    process_udf: Optional[str] = None
    process_udf_rule: Literal["$gt", "$lt", "$eq"] = None
    process_udf_value: Optional[str] = None


class StepsQuery(ListQuery):
    workflow: Optional[str] = None
    step_type: Optional[str] = None
