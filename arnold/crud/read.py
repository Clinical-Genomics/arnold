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
    artifact_udf_query_type: Optional[list[Literal["string", "double", "int"]]] = None,
    process_udf: list[Optional[str]] = None,
    process_udf_rule: list[Literal["$gt", "$lt", "$eq"]] = None,
    process_udf_value: list[Optional[str]] = None,
    process_udf_query_type: list[Literal["string", "double", "int"]] = None,
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
        {"workflow": workflow} if workflow is not None else None,
        {"step_type": step_type} if step_type is not None else None,
        {"well_position": well_position} if well_position is not None else None,
        {"artifact_name": artifact_name} if artifact_name is not None else None,
        {"container_name": container_name} if container_name is not None else None,
        {"container_id": container_id} if container_id is not None else None,
        {"container_type": container_type} if container_type is not None else None,
        {"index_name": index_name} if index_name is not None else None,
    ]
    query_pipe = list(filter(None, query_pipe))

    if artifact_udf and artifact_udf_rule and artifact_udf_query_type:
        udf_filters: list[str] = join_udf_rules(
            udf_type="artifact",
            udf_names=artifact_udf,
            udf_rules=artifact_udf_rule,
            udf_values=artifact_udf_value,
            udf_query_type=artifact_udf_query_type,
        )
        query_pipe += udf_filters

    if process_udf and process_udf_rule and process_udf_query_type:
        udf_filters: list[str] = join_udf_rules(
            udf_type="process",
            udf_names=process_udf,
            udf_rules=process_udf_rule,
            udf_values=process_udf_value,
            udf_query_type=process_udf_query_type,
        )
        query_pipe += udf_filters
    skip, limit = paginate(page_size=page_size, page_num=page_num)
    raw_steps: Iterable[dict] = (
        adapter.step_collection.find({"$and": query_pipe} if query_pipe else None)
        .sort(sort_key, SORT_TABLE.get(sort_direction))
        .skip(skip)
        .limit(limit)
    )

    return parse_obj_as(List[Step], list(raw_steps))


def find_sample_fields(adapter: ArnoldAdapter) -> list[str]:
    """"""

    pipe = [
        {"$project": {"arrayofkeyvalue": {"$objectToArray": "$$ROOT"}}},
        {"$unwind": "$arrayofkeyvalue"},
        {"$group": {"_id": None, "sample_fields": {"$addToSet": "$arrayofkeyvalue.k"}}},
    ]
    try:
        aggregation_result = list(adapter.step_collection.aggregate(pipe))
        return aggregation_result[0].get("sample_fields")
    except:
        return []


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
        {
            "$project": {
                "arrayofkeyvalue.udf": "$arrayofkeyvalue.k",
                "arrayofkeyvalue.type": {"$type": "$arrayofkeyvalue.v"},
            }
        },
        {"$group": {"_id": None, "all_udfs": {"$addToSet": "$arrayofkeyvalue"}}},
    ]
    print("kjhkjhkjhökjhkjl")
    print(pipe)
    try:
        aggregation_result = list(adapter.step_collection.aggregate(pipe))
        return aggregation_result[0].get("all_udfs")
    except:
        return []


def query_trend_sample_fields(
    adapter: ArnoldAdapter,
    year: int,
    field: str,
    group: Optional[str],
):

    match = {
        "$match": {
            "received_date": {"$exists": "True"},
            field: {"$exists": "True"},
        }
    }
    project = {
        "$project": {
            "month": {"$month": "$received_date"},
            "year": {"$year": "$received_date"},
            field: 1,
        }
    }
    match_year = {"$match": {"year": year}}
    group_by = {
        "$group": {
            "_id": {"month": "$month"},
            field: {"$push": f"${field}"},
        }
    }

    if group:
        match["$match"][group] = {"$exists": "True"}
        project["$project"][group] = 1
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [match, project, match_year, group_by]
    try:
        return list(adapter.sample_collection.aggregate(pipe))
    except:
        return []


def query_trend_step_fields(
    adapter: ArnoldAdapter,
    year: int,
    workflow: str,
    step_type: str,
    field: str,
    group: Optional[str],
):

    lookup = {
        "$lookup": {
            "from": "sample",
            "localField": "sample_id",
            "foreignField": "_id",
            "as": "sample",
        }
    }
    unwind = {"$unwind": {"path": "$sample"}}
    match = {
        "$match": {
            "date_run": {"$exists": "True"},
            field: {"$exists": "True"},
            "workflow": workflow,
            "step_type": step_type,
        }
    }
    project = {
        "$project": {
            "month": {"$month": "$date_run"},
            "year": {"$year": "$date_run"},
            field: 1,
        }
    }
    match_year = {"$match": {"year": year}}
    group_by = {
        "$group": {
            "_id": {"month": "$month"},
            field.replace(".", "_"): {"$push": f"${field}"},
        }
    }

    if group:
        match["$match"][f"sample.{group}"] = {"$exists": "True"}
        project["$project"][group] = f"$sample.{group}"
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [lookup, unwind, match, project, match_year, group_by]
    try:
        return list(adapter.step_collection.aggregate(pipe))
    except:
        return []


def query_compare(
    adapter: ArnoldAdapter,
    workflow: str = "TWIST",
    step_type_x: str = "aliquot_samples_for_enzymatic_fragmentation",
    step_type_y: str = "capture_and_wash",
    udf_x: str = "artifact_udfs.amount_needed",
    udf_y: str = "artifact_udfs.library_size_pre_hyb",
    # group: str = "sample.application",
) -> list:
    pipe = [
        {
            "$match": {
                "$or": [
                    {"step_type": step_type_x},
                    {"step_type": step_type_y},
                ],
                "workflow": workflow,
            }
        },
        {
            "$project": {
                "prep_id": 1,
                "step_type": 1,
                udf_x: 1,
                udf_y: 1,
            }
        },
        {
            "$group": {
                "_id": {"prep_id": "$prep_id"},
                "artifact_udfs": {"$push": "$artifact_udfs"},
                "step_type": {"$push": "$step_type"},
            }
        },
    ]
    try:
        return list(adapter.step_collection.aggregate(pipe))
    except:
        return []
