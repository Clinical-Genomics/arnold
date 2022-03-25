from typing import Optional, List, Literal, Iterable

from pydantic import parse_obj_as

from arnold.constants import SORT_TABLE
from arnold.crud.utils import paginate, join_udf_rules
from arnold.exceptions import MissingResultsError
from arnold.models.database.step import Step
from arnold.models.database.sample import Sample
from arnold.adapter import ArnoldAdapter


def aggregate_step(adapter: ArnoldAdapter, pipe: list) -> List:
    return list(adapter.step_collection.aggregate(pipe))


def find_sample(adapter: ArnoldAdapter, sample_id: str) -> Optional[Sample]:
    """Find one sample from the sample collection"""

    raw_sample = adapter.sample_collection.find_one({"_id": sample_id})
    if not raw_sample:
        return None
    return Sample(**raw_sample)


def find_all_samples(adapter: ArnoldAdapter) -> List[Sample]:
    """Find all samples from the step collection"""
    raw_samples = adapter.sample_collection.find()
    return parse_obj_as(List[Sample], list(raw_samples))


def find_step(adapter: ArnoldAdapter, step_id: str) -> Optional[Step]:
    """Find one step from the step collection"""

    raw_step = adapter.step_collection.find_one({"_id": step_id})
    if not raw_step:
        return None

    return Step(**raw_step)


def query_steps(
    adapter: ArnoldAdapter,
    workflow: Optional[str] = None,
    step_type: Optional[str] = None,
    artifact_udf: Optional[List[str]] = None,
    artifact_udf_rule: list[Literal["$gt", "$lt", "$eq"]] = None,
    artifact_udf_value: list[Optional[str]] = None,
    process_udf: list[Optional[str]] = None,
    process_udf_rule: list[Literal["$gt", "$lt", "$eq"]] = None,
    process_udf_value: list[Optional[str]] = None,
    sort_key: Optional[str] = "sample_id",
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend",
    well_position: Optional[str] = None,
    artifact_name: Optional[str] = None,
    container_name: Optional[str] = None,
    container_id: Optional[str] = None,
    container_type: Optional[Literal["96 well plate", "Tube"]] = None,
    index_name: Optional[str] = None,
    page_size: int = 0,
    page_num: int = 0,
) -> List[Step]:
    """
    Query steps from the sample collection.
    Pagination can be enabled with <page_size> and <page_num> options.
    No pagination enabled by default.
    """

    query_pipe = [
        {"workflow": workflow or {"$regex": ".*"}},
        {"step_type": step_type or {"$regex": ".*"}},
        {"well_position": well_position or {"$regex": ".*"}},
        {"artifact_name": artifact_name or {"$regex": ".*"}},
        {"container_name": container_name or {"$regex": ".*"}},
        {"container_id": container_id or {"$regex": ".*"}},
        {"container_type": container_type or {"$regex": ".*"}},
        {"index_name": index_name or {"$regex": ".*"}},
    ]
    if artifact_udf and artifact_udf_rule:
        udf_filters: list[str] = join_udf_rules(
            udf_type="artifact",
            udf_names=artifact_udf,
            udf_rules=artifact_udf_rule,
            udf_values=artifact_udf_value,
        )
        query_pipe += udf_filters

    if process_udf and process_udf_rule:
        udf_filters: list[str] = join_udf_rules(
            udf_type="process",
            udf_names=process_udf,
            udf_rules=process_udf_rule,
            udf_values=process_udf_value,
        )
        query_pipe += udf_filters

    skip, limit = paginate(page_size=page_size, page_num=page_num)
    raw_steps: Iterable[dict] = (
        adapter.step_collection.find({"$and": query_pipe})
        .sort(sort_key, SORT_TABLE.get(sort_direction))
        .skip(skip)
        .limit(limit)
    )

    return parse_obj_as(List[Step], list(raw_steps))


def find_step_type_udfs(
    adapter: ArnoldAdapter, workflow: str, step_type: str, udf_from: Literal["process", "artifact"]
) -> list[str]:
    """Getting available process or artifact udfs from specific step type within specific workflow"""

    pipe = [
        {
            "$match": {
                "step_type": step_type,
                "workflow": workflow,
            }
        },
        {"$replaceRoot": {"newRoot": f"${udf_from}_udfs"}},
        {"$project": {"arrayofkeyvalue": {"$objectToArray": "$$ROOT"}}},
        {"$unwind": "$arrayofkeyvalue"},
        {"$group": {"_id": None, "all_udfs": {"$addToSet": "$arrayofkeyvalue.k"}}},
    ]
    try:
        aggregation_result = list(adapter.step_collection.aggregate(pipe))
        return aggregation_result[0].get("all_udfs")
    except:
        return []
