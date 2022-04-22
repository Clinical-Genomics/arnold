u = {
    "pagination": {
        "page_size": 5,
        "page_num": 0,
        "sort_direction": "descend",
        "sort_key": "sample_id",
    },
    "step_filters": [
        {
            "workflow": "TWIST",
            "step_type": "aliquot_samples_for_enzymatic_fragmentation",
            "udf_filters": [
                {
                    "udf_name": "amount_needed",
                    "udf_rule": "$lt",
                    "udf_value": 100,
                    "udf_query_type": "bool",
                    "udf_type": "artifact",
                }
            ],
        },
        {
            "workflow": "TWIST",
            "step_type": "reception_control",
            "udf_filters": [
                {
                    "udf_name": "concentration",
                    "udf_rule": "$lt",
                    "udf_value": 100,
                    "udf_query_type": "bool",
                    "udf_type": "artifact",
                }
            ],
        },
    ],
}


p = {
    "workflow": "TWIST",
    "udf_filters": [
        {
            "udf_name": "amount_needed",
            "udf_rule": "$lt",
            "udf_value": 100,
            "udf_query_type": "bool",
            "udf_type": "artifact",
            "step_type": "aliquot_samples_for_enzymatic_fragmentation",
        },
        {
            "udf_name": "concentration",
            "udf_rule": "$lt",
            "udf_value": 100,
            "udf_query_type": "bool",
            "udf_type": "artifact",
            "step_type": "reception_control",
        },
    ],
}
