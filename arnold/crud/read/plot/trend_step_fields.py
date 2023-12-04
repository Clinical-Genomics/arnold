from typing import Optional

from arnold.adapter import ArnoldAdapter
from arnold.crud.read.plot.format_plot_data import (
    format_grouped_plot_data,
    format_plot_data,
)


def trend_step_fields(
    adapter: ArnoldAdapter,
    year: int,
    workflow: str,
    step_type: str,
    field: str,
    group: Optional[str],
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
    field_replaced_dot = field.split(".")[1]
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
            plot_data=data,
            group_field=group,
            trend_field=f"average_{field_replaced_dot}",
        )
        if group
        else format_plot_data(plot_data=data, trend_field=f"average_{field_replaced_dot}")
    )
