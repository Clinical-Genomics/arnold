from typing import List

from pymongo.results import UpdateResult
from arnold.adapter import ArnoldAdapter
from arnold.models.database import Sample, Prep
import logging

LOG = logging.getLogger(__name__)


def update_sample(adapter: ArnoldAdapter, sample: Sample) -> str:
    """Update a sample document in the database"""

    sample_id = sample.sample_id
    result: UpdateResult = adapter.sample_collection.update_one(
        {"_id": sample_id},
        {"$set": sample.dict(by_alias=True, exclude_none=True)},
        upsert=True,
    )
    if result.raw_result.get("updatedExisting"):
        LOG.info("Updated prep %s", sample_id)
    else:
        LOG.info("Added prep %s", sample_id)
    return result.upserted_id


def update_samples(adapter: ArnoldAdapter, samples: List[Sample]) -> List[str]:
    """Update sample documents in the database"""
    return [update_sample(adapter=adapter, sample=sample) for sample in samples]


def update_prep(adapter: ArnoldAdapter, prep: Prep) -> str:
    """Update a prep document in the database"""

    prep_id = prep.prep_id
    result: UpdateResult = adapter.prep_collection.update_one(
        {"_id": prep_id}, {"$set": prep.dict(by_alias=True, exclude_none=True)}, upsert=True
    )
    if result.raw_result.get("updatedExisting"):
        LOG.info("Updated prep %s", prep_id)
    else:
        LOG.info("Added prep %s", prep_id)
    return result.upserted_id


def update_preps(adapter: ArnoldAdapter, preps: List[Prep]) -> List[str]:
    """Update prep documents in the database"""
    return [update_prep(adapter=adapter, prep=prep) for prep in preps]
