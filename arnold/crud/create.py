from typing import List

from arnold.adapter import ArnoldAdapter
from arnold.models.database import LimsSample, Step
from pymongo.results import InsertManyResult, InsertOneResult
import logging

from arnold.models.database.flow_cell import FlowCell

LOG = logging.getLogger(__name__)


def create_samples(adapter: ArnoldAdapter, samples: List[LimsSample]) -> List[str]:
    """Function to create sample documents."""

    sample_dicts = [sample.dict(by_alias=True, exclude_none=True) for sample in samples]
    result: InsertManyResult = adapter.sample_collection.insert_many(sample_dicts)
    LOG.info("Added sample documents.")
    return result.inserted_ids


def create_steps(adapter: ArnoldAdapter, steps: List[Step]) -> List[str]:
    """Function to create sample document."""

    steps_dict = [step.dict(by_alias=True, exclude_none=True) for step in steps]
    result: InsertManyResult = adapter.step_collection.insert_many(steps_dict)
    LOG.info("Added steps documents.")
    return result.inserted_ids


def create_sample(adapter: ArnoldAdapter, sample: LimsSample) -> List[str]:
    """Function to create step documents."""

    result: InsertOneResult = adapter.sample_collection.insert_one(
        sample.dict(by_alias=True, exclude_none=True)
    )
    LOG.info("Updating sample %s", sample.sample_id)
    return result.inserted_id


def create_flow_cell(adapter: ArnoldAdapter, flow_cell: FlowCell) -> List[str]:
    """Function to create step documents."""

    result: InsertOneResult = adapter.flow_cell_collection.insert_one(
        flow_cell.dict(by_alias=True, exclude_none=True)
    )
    LOG.info("Updating flowcell %s", flow_cell.flow_cell_id)
    return result.inserted_id


def create_step(adapter: ArnoldAdapter, step: Step) -> List[str]:
    """Function to create step document."""

    result: InsertOneResult = adapter.step_collection.insert_one(
        step.dict(by_alias=True, exclude_none=True)
    )
    LOG.info("Updating step %s", step.step_id)
    return result.inserted_id
