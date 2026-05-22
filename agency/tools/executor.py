"""Dispatcher: mappa nome tool → funzione Python e la esegue."""
from __future__ import annotations

from typing import Any

import anthropic

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
from .performance_tracker import (
    log_weekly_metrics, get_weekly_metrics, calculate_weekly_growth,
    check_growth_target, get_performance_history,
    log_payment_decision, get_unpaid_weeks,
)

# Tool senza bisogno di client
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
    "log_weekly_metrics": log_weekly_metrics,
    "get_weekly_metrics": get_weekly_metrics,
    "calculate_weekly_growth": calculate_weekly_growth,
    "check_growth_target": check_growth_target,
    "get_performance_history": get_performance_history,
    "log_payment_decision": log_payment_decision,
    "get_unpaid_weeks": get_unpaid_weeks,
}

# Tool che richiedono il client Anthropic
_VISION_TOOLS = {"analyze_image", "analyze_trip_photos"}
_VIDEO_TOOLS = {"analyze_video", "analyze_trip_videos"}


def execute_tool(
    name: str,
    tool_input: dict[str, Any],
    client: anthropic.Anthropic | None = None,
) -> str:
    # Video tools
    if name in _VIDEO_TOOLS:
        from .video import analyze_video, analyze_trip_videos
        video_registry = {
            "analyze_video": analyze_video,
            "analyze_trip_videos": analyze_trip_videos,
        }
        fn = video_registry[name]
        try:
            return str(fn(**tool_input, client=client))
        except Exception as e:
            return f"Errore video tool '{name}': {e}"

    # Vision tools — passano il client alla funzione
    if name in _VISION_TOOLS:
        from .vision import analyze_image, analyze_trip_photos
        vision_registry = {
            "analyze_image": analyze_image,
            "analyze_trip_photos": analyze_trip_photos,
        }
        fn = vision_registry[name]
        try:
            return str(fn(**tool_input, client=client))
        except Exception as e:
            return f"Errore vision tool '{name}': {e}"

    # Tool standard
    fn = _REGISTRY.get(name)
    if fn is None:
        return f"Errore: tool sconosciuto '{name}'"
    try:
        return str(fn(**tool_input))
    except Exception as e:
        return f"Errore esecuzione tool '{name}': {e}"
