from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class Lane(BaseModel):
    name: Optional[str]
    percent_aligned_r1: Optional[float] = None
    percent_aligned_r2: Optional[float] = None
    percent_bases_q30_r1: Optional[float] = None
    percent_bases_q30_r2: Optional[float] = None
    percent_error_rate_r1: Optional[float] = None
    percent_error_rate_r2: Optional[float] = None
    percent_phasing_r1: Optional[float] = None
    percent_prephasing_r1: Optional[float] = None
    percent_prephasing_r2: Optional[float] = None
    percentpf_r1: Optional[float] = None
    percentpf_r2: Optional[float] = None
    cluster_density_r1: Optional[float] = None
    cluster_density_r2: Optional[float] = None
    intensity_cycle_1_r1: Optional[float] = None
    intensity_cycle_1_r2: Optional[float] = None
    reads_pf_millions_r1: Optional[int] = None
    reads_pf_millions_r2: Optional[int] = None
    yield_pf_giga_bases_r1: Optional[float] = None
    yield_pf_giga_bases_r2: Optional[float] = None
    percent_phasing_r2: Optional[float] = None


class FlowCell(BaseModel):
    instrument: Optional[str] = None
    date: Optional[datetime] = None
    done: Optional[bool] = None
    buffer_expiration_date: Optional[datetime] = None
    buffer_lot_number: Optional[str] = None
    buffer_part_number: Optional[str] = None
    buffer_serial_barcode: Optional[str] = None
    flow_cell_expiration_date: Optional[datetime] = None
    flow_cell_id: Optional[str] = None
    flow_cell_lot_number: Optional[str] = None
    flow_cell_mode: Optional[str] = None
    flow_cell_part_number: Optional[str] = None
    pe_cycle_kit: Optional[str] = None
    pe_expiration_date: Optional[datetime] = None
    pe_lot_number: Optional[str] = None
    pe_part_number: Optional[str] = None
    pe_serial_barcode: Optional[str] = None
    run_id: Optional[str] = None
    sbs_cycle_kit: Optional[str] = None
    sbs_expiration_date: Optional[datetime] = None
    sbs_lot_number: Optional[str] = None
    sbs_part_number: Optional[str]= None
    sbs_serial_barcode: Optional[str] = None
    lanes: Optional[List[Lane]] = None
