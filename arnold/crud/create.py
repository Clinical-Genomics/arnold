from arnold.adapter import ArnoldAdapter
from arnold.models.database import LimsSample, Step
from pymongo.results import InsertManyResult, InsertOneResult
import logging

from arnold.models.database.case.case import Case
from arnold.models.database.flow_cell import FlowCell

LOG = logging.getLogger(__name__)


def create_samples(adapter: ArnoldAdapter, samples: list[LimsSample]) -> list[str]:
    """Function to create sample documents."""

    sample_dicts = [
        sample.model_dump(by_alias=True, exclude_none=True) for sample in samples
    ]
    result: InsertManyResult = adapter.sample_collection.insert_many(sample_dicts)
    LOG.info("Added sample documents.")
    return result.inserted_ids


def create_steps(adapter: ArnoldAdapter, steps: list[Step]) -> list[str]:
    """Function to create sample document."""

    steps_dict = [step.model_dump(by_alias=True, exclude_none=True) for step in steps]
    result: InsertManyResult = adapter.step_collection.insert_many(steps_dict)
    LOG.info("Added steps documents.")
    return result.inserted_ids


def create_sample(adapter: ArnoldAdapter, sample: LimsSample) -> list[str]:
    """Function to create step documents."""

    result: InsertOneResult = adapter.sample_collection.insert_one(
        sample.model_dump(by_alias=True, exclude_none=True)
    )
    LOG.info(f"Updating sample {sample.sample_id}")
    return result.inserted_id


def create_flow_cell(adapter: ArnoldAdapter, flow_cell: FlowCell) -> list[str]:
    """Function to create step documents."""

    result: InsertOneResult = adapter.flow_cell_collection.insert_one(
        flow_cell.model_dump(by_alias=True, exclude_none=True)
    )
    LOG.info(f"Updating flowcell {flow_cell.flow_cell_id}")
    return result.inserted_id


def create_step(adapter: ArnoldAdapter, step: Step) -> list[str]:
    """Function to create step document."""

    result: InsertOneResult = adapter.step_collection.insert_one(
        step.model_dump(by_alias=True, exclude_none=True)
    )
    LOG.info(f"Updating step {step.step_id}")
    return result.inserted_id


def create_case(case: Case, adapter: ArnoldAdapter) -> list[str]:
    """Create a case document in the database."""
    case_json: dict = case.model_dump()
    result: InsertOneResult = adapter.case_collection.insert_one(document=case_json)
    LOG.info(f"Updating case {case.id}")
    return result.inserted_id
