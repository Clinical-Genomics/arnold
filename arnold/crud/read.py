from beanie import PydanticObjectId
from fastapi.exceptions import HTTPException

from arnold.models.database.prep.prep import Prep
from arnold.models.database.sample import Sample

from starlette import status


async def find_sample(sample_id: PydanticObjectId) -> Sample:
    sample = await Sample.get(sample_id)
    if sample is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sample not found")
    return sample


async def find_prep(prep_id: PydanticObjectId) -> Prep:
    prep = await Prep.get(prep_id)
    if prep is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="prep not found")
    return prep
