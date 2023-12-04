def format_plot_data(plot_data: list, trend_field):
    """Function to format raw aggregated time series"""
    ordered_plot_data = {"trend_field": [], "month": [], "group": None}
    for datapoint in plot_data:
        month = datapoint["_id"]["month"]
        trend_value = datapoint[trend_field]
        ordered_plot_data["y"].append(trend_value)
        ordered_plot_data["x"].append(month)
        continue

    return [ordered_plot_data]


def format_grouped_plot_data(plot_data: list, group_field, trend_field):
    """Function to format raw grouped aggregated time series"""

    grouped_plottdata = {}
    for datapoint in plot_data:
        group = datapoint["_id"][group_field]
        month = datapoint["_id"]["month"]
        trend_value = datapoint[trend_field]
        if group in grouped_plottdata:
            grouped_plottdata[group][trend_field].append(trend_value)
            grouped_plottdata[group]["month"].append(month)
            continue
        grouped_plottdata[group] = {
            trend_field: [trend_value],
            "month": [month],
            "group": group,
        }

    return [value for group, value in grouped_plottdata.items()]
