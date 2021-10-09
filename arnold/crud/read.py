from typing import Optional, List
from pydantic import parse_obj_as

from arnold.models.database.step import Step
from arnold.models.database.sample import Sample
from arnold.adapter import ArnoldAdapter


def find_sample(adapter: ArnoldAdapter, sample_id: str) -> Optional[Sample]:
    """Find one sample from the sample collection"""

    raw_sample = adapter.sample_collection.find_one({"_id": sample_id})
    if not raw_sample:
        return None
    return Sample(**raw_sample)


def find_all_samples(adapter: ArnoldAdapter) -> List[Sample]:
    """Find all samples from the step collection"""
    raw_samples = adapter.sample_collection.find()
    return parse_obj_as(List[Sample], list(raw_samples))


def find_step(adapter: ArnoldAdapter, step_id: str) -> Optional[Step]:
    """Find one step from the step collection"""

    raw_step = adapter.step_collection.find_one({"_id": step_id})
    if not raw_step:
        return None

    return Step(**raw_step)


def find_all_steps(adapter: ArnoldAdapter) -> List[Step]:
    """Find all steps from the step collection"""

    raw_steps = adapter.step_collection.find()

    return parse_obj_as(List[Step], list(raw_steps))
