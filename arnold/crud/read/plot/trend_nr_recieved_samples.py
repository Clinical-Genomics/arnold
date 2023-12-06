from typing import Optional

from arnold.adapter import ArnoldAdapter
from arnold.crud.read.plot.format_plot_data import (
    format_grouped_plot_data,
    format_plot_data,
)


def trend_nr_samples_per_month(
    adapter: ArnoldAdapter,
    year: int,
    group: Optional[str],
) -> list:
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
            "nr_samples": {"$sum": 1},
        }
    }

    if group:
        match["$match"][group] = {"$exists": "True"}
        project["$project"][group] = 1
        group_by["$group"]["_id"][group] = f"${group}"

    pipe = [match, project, match_year, group_by]
    data = list(adapter.sample_collection.aggregate(pipe))
    return (
        format_grouped_plot_data(plot_data=data, group_field=group, trend_field="nr_samples")
        if group
        else format_plot_data(plot_data=data, trend_field="nr_samples")
    )
