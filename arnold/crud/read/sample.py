from typing import Optional, List

from pydantic import parse_obj_as

from arnold.adapter import ArnoldAdapter
from arnold.models.database import Sample


def find_sample(adapter: ArnoldAdapter, sample_id: str) -> Optional[Sample]:
    """Find one sample from the sample collection"""

    raw_sample = adapter.sample_collection.find_one({"_id": sample_id})
    if not raw_sample:
        return None
    return Sample(**raw_sample)


def find_all_samples(adapter: ArnoldAdapter) -> List[Sample]:
    """Find all samples from the step collection"""
    raw_samples = adapter.sample_collection.find()
    return [Sample(**raw_sample) for raw_sample in raw_samples]
