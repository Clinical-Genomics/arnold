from typing import Tuple, Optional, Literal

from arnold.models.responce_models import UDFFilter


def paginate(page_size: int, page_num: int) -> Tuple[int, int]:
    """Calculate number of documents to skip"""
    if not page_size:
        return 0, 0
    if not page_num:
        return 0, page_size
    skip = page_size * (page_num - 1)
    return skip, page_size


def join_udf_rules(udf_filters: Optional[list[UDFFilter]]) -> list:
    """Joining udf rules into query strings"""
    udf_queries = []
    for udf_filter in udf_filters:
        udf_value = udf_filter.udf_value
        if udf_filter.udf_query_type != "string":
            try:
                udf_value = float(udf_filter.udf_value)
            except:
                pass
        udf_queries.append(
            {f"{udf_filter.udf_type}_udfs.{udf_filter.udf_name}": {udf_filter.udf_rule: udf_value}}
        )
    return udf_queries
