from typing import List

from arnold.adapter import ArnoldAdapter
from arnold.models.database import Sample, Prep
from pymongo.results import InsertManyResult, InsertOneResult
import logging

LOG = logging.getLogger(__name__)


def create_samples(adapter: ArnoldAdapter, samples: List[Sample]) -> List[str]:
    """Function to create sample documents."""

    sample_dicts = [sample.dict(by_alias=True, exclude_none=True) for sample in samples]
    result: InsertManyResult = adapter.sample_collection.insert_many(sample_dicts)
    LOG.info("Added sample documents.")
    return result.inserted_ids


def create_preps(adapter: ArnoldAdapter, preps: List[Prep]) -> List[str]:
    """Function to create sample document."""

    preps_dict = [prep.dict(by_alias=True, exclude_none=True) for prep in preps]
    result: InsertManyResult = adapter.prep_collection.insert_many(preps_dict)
    LOG.info("Added preps documents.")
    return result.inserted_ids


def create_sample(adapter: ArnoldAdapter, sample: Sample) -> List[str]:
    """Function to create prep documents."""

    result: InsertOneResult = adapter.sample_collection.insert_one(
        sample.dict(by_alias=True, exclude_none=True)
    )
    LOG.info("Updating sample %s", sample.sample_id)
    return result.inserted_id


def create_prep(adapter: ArnoldAdapter, prep: Prep) -> List[str]:
    """Function to create prep document."""

    result: InsertOneResult = adapter.prep_collection.insert_one(
        prep.dict(by_alias=True, exclude_none=True)
    )
    LOG.info("Updating prep %s", prep.prep_id)
    return result.inserted_id
