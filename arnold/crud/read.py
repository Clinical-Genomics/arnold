from typing import Optional, List, Literal, Iterable

import pymongo
from pydantic import parse_obj_as
from pymongo.command_cursor import CommandCursor

from arnold.crud.utils import paginate
from arnold.models.database.step import Step
from arnold.models.database.sample import Sample
from arnold.adapter import ArnoldAdapter


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


def find_all_steps(adapter: ArnoldAdapter) -> List[Step]:
    """Find all steps from the step collection"""

    raw_steps = adapter.step_collection.find()

    return parse_obj_as(List[Step], list(raw_steps))


sort_table = {"ascend": pymongo.ASCENDING, "descend": pymongo.DESCENDING}


def query_steps(
    adapter: ArnoldAdapter,
    workflow: Optional[str] = None,
    step_type: Optional[str] = None,
    artifact_udf: Optional[str] = None,
    artifact_udf_rule: Literal["$gt", "$lt", "$eq"] = None,
    artifact_udf_value: Optional[str] = None,
    process_udf: Optional[str] = None,
    process_udf_rule: Literal["$gt", "$lt", "$eq"] = None,
    process_udf_value: Optional[str] = None,
    sort_key: Optional[str] = "sample_id",
    sort_direction: Optional[Literal["ascend", "descend"]] = "descend",
    page_size: int = 0,
    page_num: int = 0,
) -> List[Step]:
    """
    Query samples from the sample collection.
    Pagination can be enabled with <page_size> and <page_num> options.
    No pagination enabled by default.
    """

    query_pipe = [
        {"workflow": workflow or {"$regex": ".*"}},
        {"step_type": step_type or {"$regex": ".*"}},
    ]
    if artifact_udf and artifact_udf_rule:
        query_pipe.append(
            {f"artifact_udfs.{artifact_udf}": {artifact_udf_rule: int(artifact_udf_value)}}
        )
    if process_udf and process_udf_rule:
        query_pipe.append({f"proces_udfs.{process_udf}": {process_udf_rule: process_udf_value}})

    skip, limit = paginate(page_size=page_size, page_num=page_num)
    raw_steps: Iterable[dict] = (
        adapter.step_collection.find({"$and": query_pipe})
        .sort(sort_key, sort_table.get(sort_direction))
        .skip(skip)
        .limit(limit)
    )

    return parse_obj_as(List[Step], list(raw_steps))


def find_step_type_process_udfs(
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
    aggregation_result = list(adapter.step_collection.aggregate(pipe))
    if not aggregation_result:
        raise  ## fix error
    return aggregation_result[0].get("all_udfs")
