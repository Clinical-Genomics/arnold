from typing import Optional, List

from pydantic import parse_obj_as

from arnold.models.database.flow_cell import FlowCell
from arnold.adapter import ArnoldAdapter


def find_flow_cell(adapter: ArnoldAdapter, flow_cell_id: str) -> Optional[FlowCell]:
    """Find one flow_cell from the flow_cell collection"""

    raw_flow_cell = adapter.flow_cell_collection.find_one({"flow_cell_id": flow_cell_id})
    if not raw_flow_cell:
        return None
    return FlowCell(**raw_flow_cell)


def find_all_flow_cells(adapter: ArnoldAdapter) -> List[FlowCell]:
    """Find all flow_cells from the step collection"""
    raw_flow_cells = adapter.flow_cell_collection.find()
    return parse_obj_as(List[FlowCell], list(raw_flow_cells))
