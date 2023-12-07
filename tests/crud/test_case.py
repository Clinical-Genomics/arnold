"""Tests for the CRUD module for cases."""
from arnold.adapter import ArnoldAdapter
from arnold.crud.create import create_case
from arnold.crud.read.case import get_case
from arnold.models.database.case import Case


def test_create_case(mock_adapter: ArnoldAdapter, balsamic_case_json: dict):
    """Test creating a case in the database."""
    # GIVEN a case document
    case: Case = Case.model_validate(balsamic_case_json)

    # WHEN creating a case in the database
    create_case(case=case, adapter=mock_adapter)

    # THEN a case is added
    new_case: Case = mock_adapter.case_collection.find_one({"id": case.id})
    assert new_case


def test_get_case(mock_adapter: ArnoldAdapter, balsamic_case_json: dict):
    """Test returning a case in the database."""
    # GIVEN a case document in the database
    case: Case = Case.model_validate(balsamic_case_json)
    create_case(case=case, adapter=mock_adapter)

    # WHEN retrieving a case
    found_case: Case = get_case(case_id=case.id, adapter=mock_adapter)

    # THEN the case is returned
    assert found_case
    assert found_case.id == case.id
