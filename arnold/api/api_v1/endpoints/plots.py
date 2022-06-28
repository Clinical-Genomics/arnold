import datetime as dt
from typing import Optional

from pydantic import Field

from arnold.adapter import ArnoldAdapter

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/received")
def received(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    date_min: Optional[dt.date] = dt.date.min,
    date_max: Optional[dt.date] = dt.date.max,
):
    samples = adapter.sample_collection.find(
        [
            {
                "$match": {
                    "delivery_date": {"$exists": 1},
                    "received_date": {"$gte": date_min.isoformat(), "$lte": date_max.isoformat()},
                }
            },
            {
                "$project": {
                    "received_date": 1,
                    "sample_id": 1,
                    "tag": {"$substr": ["$application", 0, 3]},
                    "received_year": {"$year": "$received_date"},
                    "received_month": {"$month": "$received_date"},
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": "$received_year",
                        "month": "$received_month",
                        "tag": "$tag",
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": -1}},
        ]
    )

    return list(samples)
