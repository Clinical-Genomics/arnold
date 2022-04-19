from arnold.adapter import ArnoldAdapter
from arnold.crud import create, update, read
from arnold.models.database.flow_cell import FlowCell
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging

from arnold.settings import get_arnold_adapter

LOG = logging.getLogger(__name__)

router = APIRouter()


@router.get("/flow_cell/{flow_cell_id}", response_model=FlowCell)
def get_flow_cell(
    flow_cell_id: str,
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """fetch a flow_cell by flow_cell id"""
    flow_cell: FlowCell = read.find_flow_cell(flow_cell_id=flow_cell_id, adapter=adapter)
    return flow_cell


@router.get("/flow_cells/", response_model=List[FlowCell])
def get_flow_cells(
    adapter: ArnoldAdapter = Depends(get_arnold_adapter),
):
    """Get all flow_cells"""
    flow_cells: List[FlowCell] = read.find_all_flow_cells(adapter=adapter)

    return flow_cells


@router.post("/flow_cell/")
def create_flow_cell(
    flow_cell: FlowCell, adapter: ArnoldAdapter = Depends(get_arnold_adapter)
) -> JSONResponse:
    if read.find_flow_cell(flow_cell_id=flow_cell.flow_cell_id, adapter=adapter):
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content="flow_cell already in database"
        )
    try:
        create.create_flow_cell(adapter=adapter, flow_cell=flow_cell)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=f"exception {e} ",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"flow_cell {flow_cell.flow_cell_id} inserted to db"
    )
