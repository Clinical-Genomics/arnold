from typing import Optional, List
from pydantic import parse_obj_as

from arnold.models.database.prep.prep import Prep
from arnold.models.database.sample import Sample
from arnold.adapter import ArnoldAdapter


def find_sample(adapter: ArnoldAdapter, sample_id: str) -> Optional[Sample]:
    """Find one sample from the sample collection"""

    raw_sample = adapter.sample_collection.find_one({"_id": sample_id})
    if not raw_sample:
        return None
    return Sample(**raw_sample)


def find_all_samples(adapter: ArnoldAdapter) -> List[Sample]:
    """Find all samples from the prep collection"""
    print("hej")
    raw_samples = adapter.sample_collection.find()
    return parse_obj_as(List[Sample], list(raw_samples))


def find_prep(adapter: ArnoldAdapter, prep_id: str) -> Optional[Prep]:
    """Find one prep from the prep collection"""

    raw_prep = adapter.prep_collection.find_one({"_id": prep_id})
    if not raw_prep:
        return None

    return Prep(**raw_prep)


def find_all_preps(adapter: ArnoldAdapter) -> List[Prep]:
    """Find all preps from the prep collection"""

    raw_preps = adapter.prep_collection.find()

    return parse_obj_as(List[Prep], list(raw_preps))
