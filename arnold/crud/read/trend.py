from typing import Optional

from arnold.adapter import ArnoldAdapter


def format_plot_data(plot_data: list, trend_field):
    ordered_plot_data = {"trend_field": [], "month": [], "group": None}
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
            grouped_plottdata[group][trend_field].append(trend_value)
            grouped_plottdata[group]["month"].append(month)
            continue
        grouped_plottdata[group] = {trend_field: [trend_value], "month": [month], "group": group}

    return [value for group, value in grouped_plottdata.items()]


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
