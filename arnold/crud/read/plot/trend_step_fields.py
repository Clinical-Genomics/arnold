from typing import Optional, Literal

from arnold.adapter import ArnoldAdapter
from arnold.crud.read.plot.format_plot_data import format_grouped_plot_data, format_plot_data


def trend_step_fields(
    adapter: ArnoldAdapter,
    year: int,
    workflow: str,
    step_type: str,
    field: str,
    group: Optional[str],
    udf_type: Literal["artifact_udfs", "process_udfs"],
) -> list:

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
            f"{udf_type}.{field}": {"$exists": "True"},
            "workflow": workflow,
            "step_type": step_type,
        }
    }
    project = {
        "$project": {
            "month": {"$month": "$date_run"},
            "year": {"$year": "$date_run"},
            f"{udf_type}.{field}": 1,
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
        match["$match"][f"sample.{group}"] = {"$exists": "True"}
        project["$project"][group] = f"$sample.{group}"
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [lookup, unwind, match, project, match_year, group_by, add_average]

    data = list(adapter.step_collection.aggregate(pipe))
    print(pipe)
    return (
        format_grouped_plot_data(plot_data=data, group_field=group, trend_field=f"average_{field}")
        if group
        else format_plot_data(plot_data=data, trend_field=f"average_{field}")
    )
