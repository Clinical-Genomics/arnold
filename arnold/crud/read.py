from typing import Optional, List, Literal, Iterable

from pydantic import parse_obj_as

from arnold.constants import SORT_TABLE
from arnold.crud.paginate import paginate
from arnold.models.database.step import Step
from arnold.models.database.sample import Sample
from arnold.adapter import ArnoldAdapter
from arnold.models.api_models import (
    UDFFilter,
    StepFiltersBase,
    Pagination,
    ArtifactUDF,
    ProcessUDF,
)


def format_plot_data(plot_data: list, trend_field):
    ordered_plot_data = {"y": [], "x": [], "group": None}
    for datapoint in plot_data:
        month = datapoint["_id"]["month"]
        trend_value = datapoint[trend_field]
        ordered_plot_data["y"].append(trend_value)
        ordered_plot_data["x"].append(month)
        continue

    return [ordered_plot_data]


def format_grouped_plot_data(plot_data: list, group_field, trend_field):
    #  sorted_plot_data = sorted(plot_data, key=lambda d: d["month"])
    grouped_plottdata = {}
    for datapoint in plot_data:
        group = datapoint["_id"][group_field]
        month = datapoint["_id"]["month"]
        trend_value = datapoint[trend_field]
        if group in grouped_plottdata:
            grouped_plottdata[group]["y"].append(trend_value)
            grouped_plottdata[group]["x"].append(month)
            continue
        grouped_plottdata[group] = {"y": [trend_value], "x": [month], "group": group}

    return [value for group, value in grouped_plottdata.items()]


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


def join_udf_rules(udf_filters: Optional[list[UDFFilter]]) -> list:
    """Joining udf rules into query strings"""
    udf_queries = []
    for udf_filter in udf_filters:
        udf_value = udf_filter.udf_value
        if udf_filter.udf_query_type != "string":
            try:
                udf_value = float(udf_filter.udf_value)
            except:
                pass
        udf_queries.append(
            {f"{udf_filter.udf_type}_udfs.{udf_filter.udf_name}": {udf_filter.udf_rule: udf_value}}
        )
    return udf_queries


def query_steps(
    adapter: ArnoldAdapter,
    step_filters: StepFiltersBase,
    pagination: Pagination,
    udf_filters: Optional[list[UDFFilter]],
) -> List[Step]:
    """
    Query steps from the sample collection.
    Pagination can be enabled with <page_size> and <page_num> options.
    No pagination enabled by default.
    """
    query_pipe = [step_filters.dict(exclude_none=True)]
    query_pipe += join_udf_rules(udf_filters=udf_filters)

    skip, limit = paginate(page_size=pagination.page_size, page_num=pagination.page_num)
    raw_steps: Iterable[dict] = (
        adapter.step_collection.find({"$and": query_pipe} if query_pipe else None)
        .sort(pagination.sort_key, SORT_TABLE.get(pagination.sort_direction))
        .skip(skip)
        .limit(limit)
    )
    return parse_obj_as(List[Step], list(raw_steps))


def find_sample_fields(adapter: ArnoldAdapter) -> list[str]:
    """Endpoint to get avlible sample fields"""

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


def find_step_type_udfs_pipe(
    workflow: str, step_type: str, udf_from: Literal["process", "artifact"]
) -> list[dict]:
    """Finding available udf names and types"""

    return [
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


def find_step_type_artifact_udfs(
    adapter: ArnoldAdapter, workflow: str, step_type: str
) -> List[ArtifactUDF]:
    """Getting available artifact udfs from specific step type within specific workflow"""

    pipe = find_step_type_udfs_pipe(workflow=workflow, step_type=step_type, udf_from="artifact")
    try:
        aggregation_result = list(adapter.step_collection.aggregate(pipe))
        return parse_obj_as(List[ArtifactUDF], aggregation_result[0].get("all_udfs"))
    except:
        return []


def find_step_type_process_udfs(
    adapter: ArnoldAdapter, workflow: str, step_type: str
) -> List[ProcessUDF]:
    """Getting available artifact udfs from specific step type within specific workflow"""

    pipe = find_step_type_udfs_pipe(workflow=workflow, step_type=step_type, udf_from="process")
    try:
        aggregation_result = list(adapter.step_collection.aggregate(pipe))
        return parse_obj_as(List[ProcessUDF], aggregation_result[0].get("all_udfs"))
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
    add_average = {"$addFields": {f"average_{field}": {"$avg": f"${field}"}}}

    if group:
        match["$match"][group] = {"$exists": "True"}
        project["$project"][group] = 1
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [match, project, match_year, group_by, add_average]
    data = list(adapter.sample_collection.aggregate(pipe))
    return (
        format_grouped_plot_data(plot_data=data, group_field=group, trend_field=f"average_{field}")
        if group
        else format_plot_data(plot_data=data, trend_field=f"average_{field}")
    )


def query_nr_samples_per_month(
    adapter: ArnoldAdapter,
    year: int,
    group: Optional[str],
):

    match = {
        "$match": {
            "received_date": {"$exists": "True"},
        }
    }
    project = {
        "$project": {
            "month": {"$month": "$received_date"},
            "year": {"$year": "$received_date"},
        }
    }
    match_year = {"$match": {"year": year}}
    group_by = {
        "$group": {
            "_id": {"month": "$month"},
            "count": {"$sum": 1},
        }
    }

    if group:
        match["$match"][group] = {"$exists": "True"}
        project["$project"][group] = 1
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [match, project, match_year, group_by]
    data = list(adapter.sample_collection.aggregate(pipe))
    return (
        format_grouped_plot_data(plot_data=data, group_field=group, trend_field="count")
        if group
        else format_plot_data(plot_data=data, trend_field="count")
    )


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
    field_replaced_dot = field.replace(".", "_")
    group_by = {
        "$group": {
            "_id": {"month": "$month"},
            field_replaced_dot: {"$push": f"${field}"},
        }
    }
    add_average = {
        "$addFields": {f"average_{field_replaced_dot}": {"$avg": f"${field_replaced_dot}"}}
    }

    if group:
        match["$match"][f"sample.{group}"] = {"$exists": "True"}
        project["$project"][group] = f"$sample.{group}"
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [lookup, unwind, match, project, match_year, group_by, add_average]

    data = list(adapter.step_collection.aggregate(pipe))
    return (
        format_grouped_plot_data(
            plot_data=data, group_field=group, trend_field=f"average_{field_replaced_dot}"
        )
        if group
        else format_plot_data(plot_data=data, trend_field=f"average_{field_replaced_dot}")
    )


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
