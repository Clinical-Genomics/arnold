from typing import Literal

from arnold.adapter import ArnoldAdapter


def compare_step_fields(
    adapter: ArnoldAdapter,
    workflow: str,
    step_type_x: str,
    step_type_y: str,
    udf_x: str,
    udf_y: str,
    udf_type_x: Literal["artifact_udfs", "process_udfs"],
    udf_type_y: Literal["artifact_udfs", "process_udfs"],
    # group: str = "sample.application",
) -> list:
    pipe = [
        {
            "$match": {
                "$or": [{"step_type": step_type_x}, {"step_type": step_type_y}],
                "workflow": workflow,
            }
        },
        {
            "$project": {
                "prep_id": 1,
                "sample_id": 1,
                "step_type": 1,
                udf_x: f"${udf_type_x}.{udf_x}",
                udf_y: f"${udf_type_y}.{udf_y}",
            }
        },
        {
            "$group": {
                "_id": {"prep_id": "$prep_id", "sample_id": "$sample_id"},
                udf_x: {"$push": f"${udf_x}"},
                udf_y: {"$push": f"${udf_y}"},
                "step_type": {"$push": "$step_type"},
            }
        },
        {"$unwind": {"path": f"${udf_x}"}},
        {"$unwind": {"path": f"${udf_y}"}},
        {
            "$match": {
                udf_x: {"$exists": "True"},
                udf_y: {"$exists": "True"},
            }
        },
        {
            "$group": {
                "_id": 0,
                "sample_id": {"$push": "$_id.sample_id"},
                udf_x: {"$push": f"${udf_x}"},
                udf_y: {"$push": f"${udf_y}"},
            }
        },
    ]

    try:
        return list(adapter.step_collection.aggregate(pipe))
    except:
        return []
