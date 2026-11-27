"""
Z10 Matrix - Warehouse Staging & Inventory Safety Stock Allocator.
Computes reorder points, holding costs, and dynamic weather/flood buffer staging.
"""

from typing import Dict, Any, Optional


class WarehouseAllocator:
    """Manages central staging inventory and satellite branch replenishment."""

    def __init__(self):
        self.central_depot = "Central Multi-Modal Distribution Gateway"

    def calculate_branch_inventory_allocation(
        self,
        district: str,
        monthly_sales_units: float,
        unit_cost_inr: float = 650.0,
        monsoon_mode: bool = True,
        custom_buffer_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """Calculates safety stock, cycle stock, and reorder point."""
        daily_sales = monthly_sales_units / 30.0
        lead_time_days = 1.0 if any(k in district.lower() for k in ["metro", "primary", "central", "hub"]) else 2.5

        buffer_days = custom_buffer_days if custom_buffer_days is not None else (21 if monsoon_mode else 10)
        safety_stock_units = round(daily_sales * buffer_days)
        cycle_stock_units = round(daily_sales * lead_time_days * 2)
        reorder_point = round((daily_sales * lead_time_days) + safety_stock_units)

        stock_value_inr = round((safety_stock_units + cycle_stock_units) * unit_cost_inr, 2)
        required_storage_sqft = round((safety_stock_units + cycle_stock_units) * 0.45)

        return {
            "district": district.title(),
            "lead_time_days": lead_time_days,
            "monsoon_mode_active": monsoon_mode,
            "buffer_days": buffer_days,
            "daily_velocity_units": round(daily_sales, 1),
            "safety_stock_units": safety_stock_units,
            "cycle_stock_units": cycle_stock_units,
            "reorder_point_units": reorder_point,
            "allocated_inventory_value_inr": stock_value_inr,
            "recommended_backroom_sqft": required_storage_sqft,
            "replenishment_frequency": "Every 4 Days" if lead_time_days <= 2 else "Weekly Consolidated Run"
        }


warehouse_allocator = WarehouseAllocator()
