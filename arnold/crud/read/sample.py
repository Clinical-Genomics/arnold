from typing import Optional, List


from arnold.adapter import ArnoldAdapter
from arnold.models.database import LimsSample


def get_sample_by_id(adapter: ArnoldAdapter, sample_id: str) -> Optional[LimsSample]:
    """Find one sample from the sample collection."""
    raw_sample = adapter.sample_collection.find_one({"sample_id": sample_id})
    if not raw_sample:
        return None
    return LimsSample.model_validate(raw_sample)


def get_samples(adapter: ArnoldAdapter) -> List[LimsSample]:
    """Return all samples from the step collection."""
    raw_samples = adapter.sample_collection.find()
    return [LimsSample.model_validate(raw_sample) for raw_sample in raw_samples]
