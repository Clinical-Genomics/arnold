import pymongo


QUERY_RULES = {
    "string": [
        {"mongo_rule": "$eq", "readable": "equal to"},
    ],
    "int": [
        {"mongo_rule": "$lt", "readable": "less than"},
        {"mongo_rule": "$gt", "readable": "greater than"},
        {"mongo_rule": "$eq", "readable": "equal to"},
        {"mongo_rule": "$lte", "readable": "less than or equal to"},
        {"mongo_rule": "$gte", "readable": "greater than or equal to"},
    ],
    "double": [
        {"mongo_rule": "$lt", "readable": "less than"},
        {"mongo_rule": "$gt", "readable": "greater than"},
        {"mongo_rule": "$eq", "readable": "equal to"},
        {"mongo_rule": "$lte", "readable": "less than or equal to"},
        {"mongo_rule": "$gte", "readable": "greater than or equal to"},
    ],
}


SORT_TABLE = {"ascend": pymongo.ASCENDING, "descend": pymongo.DESCENDING}
