from typing import Tuple, Optional, Literal


def paginate(page_size: int, page_num: int) -> Tuple[int, int]:
    """Calculate number of documents to skip"""
    if not page_size:
        return 0, 0
    if not page_num:
        return 0, page_size
    skip = page_size * (page_num - 1)
    return skip, page_size


def join_udf_rules_(
    udf_type: Literal["process", "artifact"],
    udf_names: Optional[list[str]],
    udf_rules: Optional[list[str]],
    udf_values: Optional[list[str]],
) -> list:
    """Joining udf rules into query strings"""
    zipped_rules = list(zip(udf_names, udf_rules, udf_values))
    udf_queries = []
    for udf_name, udf_rule, udf_value in zipped_rules:
        try:
            udf_value = float(udf_value)
        except:
            pass
        udf_queries.append({f"{udf_type}_udfs.{udf_name}": {udf_rule: udf_value}})
    return udf_queries


def join_udf_rules(
    udf_type: Literal["process", "artifact"],
    udf_query_type: list[Literal["string", "double", "int"]],
    udf_names: Optional[list[str]],
    udf_rules: Optional[list[str]],
    udf_values: Optional[list[str]],
) -> list:
    """Joining udf rules into query strings"""
    zipped_rules = list(zip(udf_names, udf_rules, udf_values))
    udf_queries = []
    for udf_name, udf_rule, udf_value in zipped_rules:
        if udf_query_type != "string":
            try:
                udf_value = float(udf_value)
            except:
                pass
        udf_queries.append({f"{udf_type}_udfs.{udf_name}": {udf_rule: udf_value}})
    return udf_queries


p = [
    {
        "$addFields": {
            "aliquot_samples_library_preparation_method_1": {
                "$toString": "$artifact_udfs.amount_needed"
            }
        }
    },
    {
        "$match": {
            "step_type": "aliquot_samples_for_enzymatic_fragmentation",
            "workflow": "TWIST",
            "aliquot_samples_library_preparation_method_1": "250",
        }
    },
]
