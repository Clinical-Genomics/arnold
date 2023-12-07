"""Tests of the CRUD for the sample model."""
from arnold.adapter import ArnoldAdapter
from arnold.models.database import LimsSample
from arnold.crud.create import create_sample
from arnold.crud.read.sample import get_sample_by_id, get_samples


def test_create_sample(mock_adapter: ArnoldAdapter, valid_sample: LimsSample):
    """Test to create a sample in the database."""
    # GIVEN a sample

    # WHEN creating a sample
    create_sample(adapter=mock_adapter, sample=valid_sample)

    # THEN the sample can be returned from the database
    sample: dict = mock_adapter.sample_collection.find_one(
        {"sample_id": valid_sample.sample_id}
    )
    assert sample
    assert isinstance(sample, dict)


def test_get_sample_by_id(mock_adapter: ArnoldAdapter, valid_sample: LimsSample):
    """Test to retrieve a sample by sample id."""
    # GIVEN a database with a sample
    create_sample(adapter=mock_adapter, sample=valid_sample)
    # WHEN retrieving the sample from the database
    sample: LimsSample = get_sample_by_id(
        mock_adapter, sample_id=valid_sample.sample_id
    )
    # THEN a sample is returned
    assert isinstance(sample, LimsSample)
    assert sample.id == valid_sample.sample_id


def test_get_samples(mock_adapter: ArnoldAdapter, valid_samples):
    """Test to retrieve all samples."""
    # GIVEN a database with multiple samples
    for valid_sample in valid_samples:
        create_sample(adapter=mock_adapter, sample=valid_sample)

    # WHEN retrieving all samples
    samples: list[LimsSample] = get_samples(adapter=mock_adapter)

    # THEN all samples are returned
    assert len(samples) == len(valid_samples)
    for sample in samples:
        assert isinstance(sample, LimsSample)
