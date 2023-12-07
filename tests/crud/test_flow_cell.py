"""Test for the CRUD module for flow cells."""
from arnold.adapter import ArnoldAdapter
from arnold.crud.read.flow_cell import get_flow_cell_by_id, get_all_flow_cells
from arnold.crud.create import create_flow_cell
from arnold.models.database.flow_cell import FlowCell


def test_create_flow_cell(mock_adapter: ArnoldAdapter, valid_flow_cell: FlowCell):
    """Test to create a flow cell entry in the database."""

    # GIVEN a flow cell

    # WHEN creating a flow cell in the database
    flow_cell_id = create_flow_cell(adapter=mock_adapter, flow_cell=valid_flow_cell)

    # THEN a flow cell can be returned
    new_flow_cell = mock_adapter.flow_cell_collection.find_one({"_id": flow_cell_id})
    assert new_flow_cell


def test_get_flow_cell_by_flow_cell_id(
    mock_adapter: ArnoldAdapter, valid_flow_cell: FlowCell
):
    """Test to retrieve a flow cell from the database."""
    # GIVEN a flow cell

    # WHEN creating a flow cell in the database
    create_flow_cell(adapter=mock_adapter, flow_cell=valid_flow_cell)

    # THEN a flow cell can be returned
    new_flow_cell: FlowCell = get_flow_cell_by_id(
        adapter=mock_adapter, flow_cell_id=valid_flow_cell.flow_cell_id
    )
    assert new_flow_cell
    assert isinstance(new_flow_cell, FlowCell)


def test_get_all_flow_cells(mock_adapter: ArnoldAdapter, valid_flow_cell: FlowCell):
    """Test to get all flow cells from the database."""
    # GIVEN a database with multiple flow cells
    create_flow_cell(adapter=mock_adapter, flow_cell=valid_flow_cell)
    another_flow_cell: FlowCell = valid_flow_cell
    another_flow_cell.flow_cell_id = "FlowCell2"
    create_flow_cell(adapter=mock_adapter, flow_cell=another_flow_cell)

    # WHEN retrieving all flow cells in the database
    flow_cells: list[FlowCell] = get_all_flow_cells(adapter=mock_adapter)

    # THEN all flow cells are returned
    assert len(flow_cells) == 2
    for flow_cell in flow_cells:
        assert isinstance(flow_cell, FlowCell)
