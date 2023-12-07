from typing import Optional, List


from arnold.models.database.flow_cell import FlowCell
from arnold.adapter import ArnoldAdapter


def get_flow_cell_by_id(
    adapter: ArnoldAdapter, flow_cell_id: str
) -> Optional[FlowCell]:
    """Return a flow cell by flow cell id."""

    raw_flow_cell: FlowCell = adapter.flow_cell_collection.find_one(
        {"flow_cell_id": flow_cell_id}
    )
    if not raw_flow_cell:
        return None
    return FlowCell.model_validate(raw_flow_cell)


def get_all_flow_cells(adapter: ArnoldAdapter) -> List[FlowCell]:
    """Return all flow cells from the flow cell collection."""
    raw_flow_cells = adapter.flow_cell_collection.find()
    return [FlowCell.model_validate(flow_cell) for flow_cell in raw_flow_cells]
