"""Schema Anthropic per tutti i tool disponibili agli agenti."""
from __future__ import annotations

_ALL: dict[str, dict] = {
    # ── FILESYSTEM ──────────────────────────────────────────────────────────
    "read_file": {
        "name": "read_file",
        "description": "Leggi il contenuto di un file nel filesystem dei viaggi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Percorso del file da leggere"},
            },
            "required": ["path"],
        },
    },
    "write_file": {
        "name": "write_file",
        "description": "Scrivi o sovrascrivi un file con il contenuto fornito.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Percorso del file"},
                "content": {"type": "string", "description": "Contenuto da scrivere"},
            },
            "required": ["path", "content"],
        },
    },
    "list_files": {
        "name": "list_files",
        "description": "Elenca file e cartelle in una directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "folder": {"type": "string", "description": "Percorso della cartella"},
            },
            "required": ["folder"],
        },
    },
    "move_file": {
        "name": "move_file",
        "description": "Sposta un file da una cartella all'altra (es. da editing ad approved).",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Percorso sorgente"},
                "destination": {"type": "string", "description": "Percorso destinazione"},
            },
            "required": ["source", "destination"],
        },
    },
    "save_brief": {
        "name": "save_brief",
        "description": "Salva un brief creativo nella cartella 07_briefs del viaggio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {"type": "string", "description": "ID del viaggio"},
                "content": {"type": "string", "description": "Contenuto del brief in Markdown"},
                "filename": {"type": "string", "description": "Nome file (default: brief.md)"},
            },
            "required": ["trip_id", "content"],
        },
    },
    "save_report": {
        "name": "save_report",
        "description": "Salva un report nella cartella 06_reports del viaggio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {"type": "string", "description": "ID del viaggio"},
                "content": {"type": "string", "description": "Contenuto del report in Markdown"},
                "filename": {"type": "string", "description": "Nome file (default: report.md)"},
            },
            "required": ["trip_id", "content"],
        },
    },
    "list_trip_structure": {
        "name": "list_trip_structure",
        "description": "Mostra la struttura completa di cartelle e file di un viaggio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {"type": "string", "description": "ID del viaggio"},
            },
            "required": ["trip_id"],
        },
    },

    # ── CALCULATOR ──────────────────────────────────────────────────────────
    "calculate_cpm": {
        "name": "calculate_cpm",
        "description": "Calcola il CPM (Cost Per Mille) di una campagna.",
        "input_schema": {
            "type": "object",
            "properties": {
                "impressions": {"type": "integer", "description": "Numero di impressioni"},
                "fee": {"type": "number", "description": "Fee totale in euro"},
            },
            "required": ["impressions", "fee"],
        },
    },
    "calculate_engagement_rate": {
        "name": "calculate_engagement_rate",
        "description": "Calcola l'engagement rate da like, commenti e follower.",
        "input_schema": {
            "type": "object",
            "properties": {
                "likes": {"type": "integer", "description": "Numero di like"},
                "comments": {"type": "integer", "description": "Numero di commenti"},
                "followers": {"type": "integer", "description": "Numero di follower"},
            },
            "required": ["likes", "comments", "followers"],
        },
    },
    "estimate_influencer_fee": {
        "name": "estimate_influencer_fee",
        "description": "Stima la fee di mercato per un influencer in base a follower, engagement, piattaforma e tipo di contenuto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "followers": {"type": "integer", "description": "Numero di follower"},
                "engagement_rate": {"type": "number", "description": "Tasso di engagement (%)"},
                "platform": {"type": "string", "description": "Piattaforma (instagram, tiktok, youtube, ecc.)"},
                "content_type": {"type": "string", "description": "Tipo contenuto (reel, video, post, story, ecc.)"},
            },
            "required": ["followers", "engagement_rate", "platform", "content_type"],
        },
    },
    "calculate_roi": {
        "name": "calculate_roi",
        "description": "Calcola il ROI di una campagna sponsorizzata.",
        "input_schema": {
            "type": "object",
            "properties": {
                "revenue": {"type": "number", "description": "Revenue generata dalla campagna in euro"},
                "costs": {"type": "number", "description": "Costi totali della campagna in euro"},
            },
            "required": ["revenue", "costs"],
        },
    },
    "calculate_monthly_revenue_breakdown": {
        "name": "calculate_monthly_revenue_breakdown",
        "description": "Calcola il breakdown mensile del revenue per stream di monetizzazione.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sponsorships": {"type": "number", "description": "Revenue da sponsorizzazioni (€)"},
                "platforms": {"type": "number", "description": "Revenue da monetizzazione piattaforme (€)"},
                "affiliates": {"type": "number", "description": "Revenue da affiliate marketing (€)"},
                "products": {"type": "number", "description": "Revenue da prodotti digitali (€)"},
            },
            "required": ["sponsorships", "platforms", "affiliates", "products"],
        },
    },

    # ── BRAND REGISTRY ──────────────────────────────────────────────────────
    "register_brand": {
        "name": "register_brand",
        "description": "Registra un nuovo brand nel database dell'agenzia.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nome del brand"},
                "contact": {"type": "string", "description": "Email o contatto del brand"},
                "niche": {"type": "string", "description": "Nicchia/settore del brand"},
                "budget_range": {"type": "string", "description": "Range budget tipico (es. €500-2000)"},
                "notes": {"type": "string", "description": "Note aggiuntive (opzionale)"},
            },
            "required": ["name", "contact", "niche", "budget_range"],
        },
    },
    "get_brand": {
        "name": "get_brand",
        "description": "Recupera le informazioni di un brand dal database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nome del brand"},
            },
            "required": ["name"],
        },
    },
    "list_brands": {
        "name": "list_brands",
        "description": "Elenca tutti i brand nel database, filtrabile per nicchia.",
        "input_schema": {
            "type": "object",
            "properties": {
                "niche": {"type": "string", "description": "Filtra per nicchia (lascia vuoto per tutti)"},
            },
            "required": [],
        },
    },
    "log_deal": {
        "name": "log_deal",
        "description": "Registra un deal/collaborazione nel database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "brand": {"type": "string", "description": "Nome del brand"},
                "creator": {"type": "string", "description": "Nome del creator"},
                "deal_type": {"type": "string", "description": "Tipo di deal (es. reel, video, post)"},
                "fee": {"type": "number", "description": "Fee concordata in euro"},
                "status": {"type": "string", "description": "Stato: proposto|negoziazione|confermato|completato|rifiutato"},
                "notes": {"type": "string", "description": "Note aggiuntive"},
            },
            "required": ["brand", "creator", "deal_type", "fee", "status"],
        },
    },
    "get_deal_history": {
        "name": "get_deal_history",
        "description": "Recupera lo storico dei deal, filtrabile per brand o creator.",
        "input_schema": {
            "type": "object",
            "properties": {
                "brand": {"type": "string", "description": "Filtra per nome brand (opzionale)"},
                "creator": {"type": "string", "description": "Filtra per nome creator (opzionale)"},
            },
            "required": [],
        },
    },
    "update_deal_status": {
        "name": "update_deal_status",
        "description": "Aggiorna lo status di un deal esistente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "deal_id": {"type": "string", "description": "ID del deal (es. deal_0001)"},
                "status": {"type": "string", "description": "Nuovo status"},
                "notes": {"type": "string", "description": "Note aggiuntive"},
            },
            "required": ["deal_id", "status"],
        },
    },

    # ── CONTENT CATALOG ─────────────────────────────────────────────────────
    "search_trips": {
        "name": "search_trips",
        "description": "Cerca viaggi nel catalogo per destinazione, creator o tag.",
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "Filtra per destinazione"},
                "creator": {"type": "string", "description": "Filtra per nome creator"},
                "tag": {"type": "string", "description": "Filtra per tag"},
            },
            "required": [],
        },
    },
    "get_content_inventory": {
        "name": "get_content_inventory",
        "description": "Inventario completo di tutti i file presenti nelle cartelle di un viaggio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {"type": "string", "description": "ID del viaggio"},
            },
            "required": ["trip_id"],
        },
    },
    "find_approved_content": {
        "name": "find_approved_content",
        "description": "Trova i contenuti approvati pronti per la pubblicazione, filtrabile per piattaforma.",
        "input_schema": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "description": "Piattaforma (instagram, tiktok, youtube, ecc.) — opzionale"},
                "trip_id": {"type": "string", "description": "ID viaggio specifico — opzionale"},
            },
            "required": [],
        },
    },
}


def get_tools_by_name(names: list[str]) -> list[dict]:
    """Restituisce le definizioni Anthropic per i tool richiesti."""
    return [_ALL[n] for n in names if n in _ALL]


# Gruppi predefiniti per comodità
FILESYSTEM_TOOLS = [
    "read_file", "write_file", "list_files", "move_file",
    "save_brief", "save_report", "list_trip_structure",
]
CALCULATOR_TOOLS = [
    "calculate_cpm", "calculate_engagement_rate", "estimate_influencer_fee",
    "calculate_roi", "calculate_monthly_revenue_breakdown",
]
BRAND_REGISTRY_TOOLS = [
    "register_brand", "get_brand", "list_brands",
    "log_deal", "get_deal_history", "update_deal_status",
]
CONTENT_CATALOG_TOOLS = [
    "search_trips", "get_content_inventory", "find_approved_content",
]
