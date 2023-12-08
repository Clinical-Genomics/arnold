"""Tests of the CRUD for the step model."""
from arnold.adapter import ArnoldAdapter
from arnold.crud.create import create_step
from arnold.crud.read.step import get_step
from arnold.models.database import Step


def test_create_step(valid_step: Step, mock_adapter: ArnoldAdapter):
    """Test to create a step in the database."""
    # GIVEN a valid step

    # WHEN creating a step in the database
    create_step(adapter=mock_adapter, step=valid_step)

    # THEN a step can be retrieved from the database
    step: dict = mock_adapter.step_collection.find_one({"prep_id": valid_step.prep_id})
    assert step
    assert isinstance(step, dict)
    assert Step.model_validate(step).prep_id == valid_step.prep_id


def test_get_step(valid_step: Step, mock_adapter: ArnoldAdapter):
    """Test to retrieve a step in the database."""
    # GIVEN a database with a step
    create_step(adapter=mock_adapter, step=valid_step)

    # WHEN retrieving the step from the database
    step: Step = get_step(adapter=mock_adapter, step_id=valid_step.step_id)

    # THEN a step is returned
    assert isinstance(step, Step)
    assert step.step_id == valid_step.step_id
