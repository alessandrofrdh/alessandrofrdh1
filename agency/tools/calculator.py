"""Calcolatori finanziari: revenue, ROI, fee influencer, CPM."""
from __future__ import annotations


def calculate_cpm(impressions: int, fee: float) -> str:
    if impressions <= 0:
        return "Errore: impressioni deve essere > 0"
    cpm = (fee / impressions) * 1000
    return (
        f"CPM: €{cpm:.2f}\n"
        f"  Fee: €{fee:,.2f}  /  Impressioni: {impressions:,}"
    )


def calculate_engagement_rate(likes: int, comments: int, followers: int) -> str:
    if followers <= 0:
        return "Errore: followers deve essere > 0"
    total = likes + comments
    rate = (total / followers) * 100
    label = "ottimo (>3%)" if rate > 3 else "nella media (1-3%)" if rate > 1 else "sotto la media (<1%)"
    return (
        f"Engagement rate: {rate:.2f}%  —  {label}\n"
        f"  Like: {likes:,}  Commenti: {comments:,}  Follower: {followers:,}"
    )


def estimate_influencer_fee(
    followers: int,
    engagement_rate: float,
    platform: str,
    content_type: str,
) -> str:
    base_rates: dict[str, dict[str, float]] = {
        "instagram": {"post": 10, "reel": 15, "story": 3, "carosello": 12},
        "tiktok":    {"video": 8, "live": 5},
        "youtube":   {"video": 20, "short": 10},
        "facebook":  {"post": 5, "reel": 8},
        "linkedin":  {"post": 12, "articolo": 18},
    }
    p = platform.lower()
    c = content_type.lower()
    rates = base_rates.get(p, {"post": 8})
    base_rate = rates.get(c, next(iter(rates.values())))

    base_fee = (followers / 1000) * base_rate
    multiplier = 1.5 if engagement_rate > 5 else 1.25 if engagement_rate > 3 else 1.0 if engagement_rate > 1 else 0.75
    fee = base_fee * multiplier

    return (
        f"Stima fee — {content_type} su {platform}\n"
        f"  Follower: {followers:,}  |  Engagement: {engagement_rate:.1f}%\n"
        f"  Range: €{fee*0.8:,.0f} — €{fee*1.3:,.0f}\n"
        f"  Fee consigliata: €{fee:,.0f}"
    )


def calculate_roi(revenue: float, costs: float) -> str:
    if costs <= 0:
        return "Errore: i costi devono essere > 0"
    roi = ((revenue - costs) / costs) * 100
    profit = revenue - costs
    label = "positivo" if roi > 0 else "negativo"
    return (
        f"ROI: {roi:.1f}%  ({label})\n"
        f"  Revenue: €{revenue:,.2f}\n"
        f"  Costi:   €{costs:,.2f}\n"
        f"  Profitto netto: €{profit:,.2f}"
    )


def calculate_monthly_revenue_breakdown(
    sponsorships: float,
    platforms: float,
    affiliates: float,
    products: float,
) -> str:
    total = sponsorships + platforms + affiliates + products
    if total == 0:
        return "Revenue totale: €0"
    lines = [f"Revenue mensile totale: €{total:,.2f}\n"]
    for name, amount in [
        ("Sponsorizzazioni", sponsorships),
        ("Monetizzazione piattaforme", platforms),
        ("Affiliate marketing", affiliates),
        ("Prodotti digitali", products),
    ]:
        pct = amount / total * 100
        lines.append(f"  {name:<30} €{amount:>8,.2f}  ({pct:.0f}%)")
    return "\n".join(lines)
