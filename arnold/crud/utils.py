from typing import Tuple, Optional, Literal


def paginate(page_size: int, page_num: int) -> Tuple[int, int]:
    """Calculate number of documents to skip"""
    if not page_size:
        return 0, 0
    if not page_num:
        return 0, page_size
    skip = page_size * (page_num - 1)
    return skip, page_size


def join_udf_rules(
    udf_type: Literal["process", "artifact"],
    udf_names: Optional[list[str]],
    udf_rules: Optional[list[str]],
    udf_values: Optional[list[str]],
) -> list:
    zipped_rules = list(zip(udf_names, udf_rules, udf_values))
    return [
        {f"{udf_type}_udfs.{udf_name}": {udf_rule: int(udf_value)}}
        for udf_name, udf_rule, udf_value in zipped_rules
    ]
