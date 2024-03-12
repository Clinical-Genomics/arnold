"""CRUD module to find entries."""


from arnold.adapter import ArnoldAdapter
from arnold.models.database.case.case import Case


def get_case(case_id: str, adapter: ArnoldAdapter) -> Case | None:
    """
    Retrieve a case document from the database.
        Raises: ValidationError
    """
    case: dict = adapter.case_collection.find_one({"case_id": case_id})
    if not case:
        return None
    return Case.model_validate(case)
