import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from arnold.adapter import ArnoldAdapter

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging
from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


class ReceivedPlotDatapointsModel(BaseModel):
    tag: str
    count: int


class ReceivedPlotModel(BaseModel):
    date: str
    datapoints: List[ReceivedPlotDatapointsModel]


@router.get("/received", response_model=List[ReceivedPlotModel])
def received(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
    date_min: Optional[dt.date] = dt.date.min,
    date_max: Optional[dt.date] = dt.date.max,
):
    samples = adapter.sample_collection.aggregate(
        [
            {
                "$match": {
                    "delivery_date": {"$exists": 1},
                    "received_date": {
                        "$gte": dt.datetime.fromordinal(date_min.toordinal()),
                        "$lte": dt.datetime.fromordinal(date_max.toordinal()),
                    },
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
                    "_id": {"tag": "$tag", "year": "$received_year", "month": "$received_month"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "year": "$_id.year",
                    "month": "$_id.month",
                    "date": {
                        "$concat": [
                            {"$substr": ["$_id.year", 0, -1]},
                            "/",
                            {"$substr": ["$_id.month", 0, -1]},
                        ]
                    },
                    "tag": "$_id.tag",
                    "count": "$count",
                    "_id": 0,
                }
            },
            {
                "$group": {
                    "_id": {"date": "$date", "year": "$year", "month": "$month"},
                    "datapoints": {"$push": "$$ROOT"},
                }
            },
            {
                "$project": {
                    "date": "$_id.date",
                    "year": "$_id.year",
                    "month": "$_id.month",
                    "datapoints": "$datapoints",
                    "_id": 0,
                }
            },
            {"$unset": ["datapoints.date", "datapoints.year", "datapoints.month"]},
            {"$sort": {"year": -1, "month": -1}},
            {"$unset": ["year", "month"]},
        ]
    )
    return list(samples)
