"""Dispatcher: mappa nome tool → funzione Python e la esegue."""
from __future__ import annotations

from typing import Any

from .filesystem import (
    read_file, write_file, list_files, move_file,
    save_brief, save_report, list_trip_structure,
)
from .calculator import (
    calculate_cpm, calculate_engagement_rate, estimate_influencer_fee,
    calculate_roi, calculate_monthly_revenue_breakdown,
)
from .brand_registry import (
    register_brand, get_brand, list_brands,
    log_deal, get_deal_history, update_deal_status,
)
from .content_catalog import (
    search_trips, get_content_inventory, find_approved_content,
)

_REGISTRY: dict[str, Any] = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files,
    "move_file": move_file,
    "save_brief": save_brief,
    "save_report": save_report,
    "list_trip_structure": list_trip_structure,
    "calculate_cpm": calculate_cpm,
    "calculate_engagement_rate": calculate_engagement_rate,
    "estimate_influencer_fee": estimate_influencer_fee,
    "calculate_roi": calculate_roi,
    "calculate_monthly_revenue_breakdown": calculate_monthly_revenue_breakdown,
    "register_brand": register_brand,
    "get_brand": get_brand,
    "list_brands": list_brands,
    "log_deal": log_deal,
    "get_deal_history": get_deal_history,
    "update_deal_status": update_deal_status,
    "search_trips": search_trips,
    "get_content_inventory": get_content_inventory,
    "find_approved_content": find_approved_content,
}


def execute_tool(name: str, tool_input: dict[str, Any]) -> str:
    fn = _REGISTRY.get(name)
    if fn is None:
        return f"Errore: tool sconosciuto '{name}'"
    try:
        result = fn(**tool_input)
        return str(result)
    except Exception as e:
        return f"Errore esecuzione tool '{name}': {e}"
