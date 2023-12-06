"""CRUD module to find entries."""


from arnold.adapter import ArnoldAdapter
from arnold.models.database.case import Case


def get_case(case_id: str, adapter: ArnoldAdapter) -> Case | None:
    """Retrieve a case document from the database."""
    case: dict = adapter.case_collection.find_one({"id": case_id})
    if not case:
        return None
    return Case.model_validate(case)
