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
    # ── VISION ──────────────────────────────────────────────────────────────
    "analyze_image": {
        "name": "analyze_image",
        "description": (
            "Analizza un'immagine con Claude vision. Valuta qualità tecnica, "
            "potenziale social, mood, palette cromatica e suggerimenti di editing."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Percorso del file immagine (jpg, png, webp, gif)",
                },
                "question": {
                    "type": "string",
                    "description": "Domanda specifica sull'immagine (opzionale, usa analisi default se omessa)",
                },
            },
            "required": ["path"],
        },
    },
    "analyze_trip_photos": {
        "name": "analyze_trip_photos",
        "description": (
            "Analizza tutte le immagini in una cartella di un viaggio. "
            "Utile per selezione foto, QC batch e briefing editoriale."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {
                    "type": "string",
                    "description": "ID del viaggio (es. 2026-06-15_marocco)",
                },
                "subfolder": {
                    "type": "string",
                    "description": "Sottocartella da analizzare (default: 01_raw/photo)",
                },
                "question": {
                    "type": "string",
                    "description": "Domanda specifica da applicare a tutte le foto (opzionale)",
                },
            },
            "required": ["trip_id"],
        },
    },

    # ── VIDEO ────────────────────────────────────────────────────────────────
    "analyze_video": {
        "name": "analyze_video",
        "description": (
            "Analizza un video estraendo frame chiave con ffmpeg e analizzandoli con Claude vision. "
            "Produce: metadati tecnici, analisi frame-by-frame, raccomandazioni di montaggio, "
            "piattaforme consigliate (TikTok/Reels/YouTube) e voto /10."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Percorso del file video (mp4, mov, avi, mkv, webm, ecc.)",
                },
                "question": {
                    "type": "string",
                    "description": "Domanda specifica da applicare ad ogni frame (opzionale)",
                },
                "num_frames": {
                    "type": "integer",
                    "description": "Numero di frame chiave da estrarre e analizzare (default: 6, max consigliato: 10)",
                },
            },
            "required": ["path"],
        },
    },
    "analyze_trip_videos": {
        "name": "analyze_trip_videos",
        "description": (
            "Analizza tutti i video in una cartella di un viaggio. "
            "Utile per selezione clip, QC batch e briefing montaggio."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "trip_id": {
                    "type": "string",
                    "description": "ID del viaggio (es. 2026-06-15_marocco)",
                },
                "subfolder": {
                    "type": "string",
                    "description": "Sottocartella da analizzare (default: 01_raw/video)",
                },
                "question": {
                    "type": "string",
                    "description": "Domanda specifica da applicare a tutti i video (opzionale)",
                },
                "num_frames": {
                    "type": "integer",
                    "description": "Frame da estrarre per ogni video (default: 4)",
                },
            },
            "required": ["trip_id"],
        },
    },
    # ── PERFORMANCE TRACKER ─────────────────────────────────────────────────
    "log_weekly_metrics": {
        "name": "log_weekly_metrics",
        "description": "Registra le metriche di performance di una settimana nel tracker.",
        "input_schema": {
            "type": "object",
            "properties": {
                "week": {"type": "integer", "description": "Numero della settimana (1-6)"},
                "metrics": {
                    "type": "object",
                    "description": "Dizionario metriche: follower_ig, follower_tiktok, follower_youtube, engagement_rate, reach, impressions, conversioni",
                },
                "notes": {"type": "string", "description": "Note aggiuntive (opzionale)"},
            },
            "required": ["week", "metrics"],
        },
    },
    "get_weekly_metrics": {
        "name": "get_weekly_metrics",
        "description": "Recupera le metriche registrate per una specifica settimana.",
        "input_schema": {
            "type": "object",
            "properties": {
                "week": {"type": "integer", "description": "Numero della settimana"},
            },
            "required": ["week"],
        },
    },
    "calculate_weekly_growth": {
        "name": "calculate_weekly_growth",
        "description": "Calcola la crescita percentuale di ogni metrica rispetto alla settimana precedente.",
        "input_schema": {
            "type": "object",
            "properties": {
                "week": {"type": "integer", "description": "Settimana da analizzare (confronta con week-1)"},
            },
            "required": ["week"],
        },
    },
    "check_growth_target": {
        "name": "check_growth_target",
        "description": "Verifica se la settimana ha raggiunto il target minimo su tutte le metriche. Ritorna RAGGIUNTO o NON RAGGIUNTO con dettaglio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "week": {"type": "integer", "description": "Settimana da verificare"},
                "target_pct": {"type": "number", "description": "Target percentuale (default: 10.0)"},
            },
            "required": ["week"],
        },
    },
    "get_performance_history": {
        "name": "get_performance_history",
        "description": "Storico completo di tutte le settimane con metriche e pagamenti.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    "log_payment_decision": {
        "name": "log_payment_decision",
        "description": "Registra la decisione di pagamento del proprietario per una settimana.",
        "input_schema": {
            "type": "object",
            "properties": {
                "week": {"type": "integer", "description": "Numero della settimana"},
                "approved": {"type": "boolean", "description": "True = pagamento approvato, False = rifiutato"},
                "reason": {"type": "string", "description": "Motivazione della decisione"},
                "amount_eur": {"type": "number", "description": "Importo in euro (0 se rifiutato)"},
            },
            "required": ["week", "approved", "reason"],
        },
    },
    "get_unpaid_weeks": {
        "name": "get_unpaid_weeks",
        "description": "Elenca le settimane con pagamento rifiutato o ancora in attesa di valutazione.",
        "input_schema": {
            "type": "object",
            "properties": {},
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
VISION_TOOLS = [
    "analyze_image", "analyze_trip_photos",
]
VIDEO_TOOLS = [
    "analyze_video", "analyze_trip_videos",
]
PERFORMANCE_TOOLS = [
    "log_weekly_metrics", "get_weekly_metrics", "calculate_weekly_growth",
    "check_growth_target", "get_performance_history",
    "log_payment_decision", "get_unpaid_weeks",
]
