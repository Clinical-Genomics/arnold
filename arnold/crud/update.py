from typing import List

from pymongo.results import UpdateResult
from arnold.adapter import ArnoldAdapter
from arnold.models.database import LimsSample, Step
import logging

LOG = logging.getLogger(__name__)


def update_sample(adapter: ArnoldAdapter, sample: LimsSample) -> str:
    """Update a sample document in the database"""

    sample_id = sample.sample_id
    result: UpdateResult = adapter.sample_collection.update_one(
        {"_id": sample_id},
        {"$set": sample.dict(by_alias=True, exclude_none=True)},
        upsert=True,
    )
    if result.raw_result.get("updatedExisting"):
        LOG.info("Updated step %s", sample_id)
    else:
        LOG.info("Added step %s", sample_id)
    return result.upserted_id


def update_samples(adapter: ArnoldAdapter, samples: List[LimsSample]) -> List[str]:
    """Update sample documents in the database"""
    return [update_sample(adapter=adapter, sample=sample) for sample in samples]


def update_step(adapter: ArnoldAdapter, step: Step) -> str:
    """Update a step document in the database"""

    step_id = step.step_id
    result: UpdateResult = adapter.step_collection.update_one(
        {"_id": step_id},
        {"$set": step.dict(by_alias=True, exclude_none=True)},
        upsert=True,
    )
    if result.raw_result.get("updatedExisting"):
        LOG.info("Updated step %s", step_id)
    else:
        LOG.info("Added step %s", step_id)
    return result.upserted_id


def update_steps(adapter: ArnoldAdapter, steps: List[Step]) -> List[str]:
    """Update step documents in the database"""
    return [update_step(adapter=adapter, step=step) for step in steps]
