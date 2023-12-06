from typing import Optional

from arnold.adapter import ArnoldAdapter
from arnold.crud.read.plot.format_plot_data import (
    format_grouped_plot_data,
    format_plot_data,
)


def trend_turn_around_times(
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
    add_average = {"$addFields": {f"average_nr_days_{field}": {"$avg": f"${field}"}}}

    if group:
        match["$match"][group] = {"$exists": "True"}
        project["$project"][group] = 1
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [match, project, match_year, group_by, add_average]
    data = list(adapter.sample_collection.aggregate(pipe))
    return (
        format_grouped_plot_data(
            plot_data=data, group_field=group, trend_field=f"average_nr_days_{field}"
        )
        if group
        else format_plot_data(plot_data=data, trend_field=f"average_nr_days_{field}")
    )
