# TravelVision Agency

Sistema multi-agente AI che replica un'agenzia marketing di 100 persone specializzata in contenuti di viaggio e monetizzazione di profili social.

## Struttura del team

| Dipartimento | Ruoli |
|---|---|
| **Executive** | CEO, COO, CMO |
| **Contenuti** | Direttore, 3× Video Editor, 3× Photo Editor, 2× Copywriter, Graphic Designer, Content Strategist |
| **Social Media** | Direttore, Instagram, TikTok, YouTube, Facebook, LinkedIn Manager, Community Manager, Scheduler, Analytics |
| **Viaggi** | Direttore, Ricercatore Destinazioni, Fotografo, Videomaker, Pianificatore Itinerari |
| **Sponsorizzazioni** | Direttore, Brand Partnership, Influencer Relations, Revenue Manager, Ad Campaign, ROI Analyst |
| **Operations** | Project Manager, File Manager, Analytics Manager, SEO Specialist, Quality Control, Archive Manager |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Inserisci ANTHROPIC_API_KEY in .env
```

## Utilizzo

### Avvio interattivo
```bash
python main.py
```

### Demo completa
```bash
python main.py demo
```

### Pianificare un viaggio
```bash
python main.py trip "Nome Creator" "Destinazione"
```

### Uso programmatico

```python
from agency import TravelVisionAgency

agency = TravelVisionAgency()

# Onboarding creator
results = agency.onboard_creator(
    creator_name="Lorenzo Viaggio",
    niche="travel avventura",
    platforms=["Instagram", "TikTok", "YouTube"],
    monthly_revenue_goal=5000.0,
    target_audience={"età": "25-35", "interessi": ["viaggi", "outdoor"]},
)

# Pianifica un viaggio di contenuto
plan = agency.plan_content_trip(
    creator_name="Lorenzo Viaggio",
    destination="Giappone",
    start_date="2026-09-01",
    duration_days=10,
    budget=5000.0,
    platforms=["Instagram", "TikTok", "YouTube"],
)
# Cartella automaticamente creata in content/trips/

# Produci contenuto
package = agency.produce_content_package(
    trip_id=plan.trip_id,
    destination="Giappone",
    platform="Instagram",
    raw_content_description="Clip del tempio Fushimi Inari all'alba...",
    creator_style="cinematico, colori vividi",
    brand_voice="autentico e curioso",
)

# Gestisci una sponsorizzazione
deal = agency.manage_sponsorship(
    creator_profile={"nome": "Lorenzo Viaggio", "nicchia": "travel"},
    brand="Sony Alpha",
    collaboration_type="review fotocamera durante viaggio",
    mode="outreach",
)
```

## Struttura cartelle viaggio

Ogni viaggio crea automaticamente:
```
content/trips/{data}_{destinazione}/
├── 01_raw/          # Materiale grezzo (foto, video, audio)
├── 02_editing/      # Lavori in corso (photo_edit, video_edit, graphics)
├── 03_approved/     # Pronti per pubblicazione (per piattaforma)
├── 04_published/    # Già pubblicati
├── 05_sponsorships/ # Brief e deliverable brand
├── 06_reports/      # Analytics e report
├── 07_briefs/       # Brief creativi e contratti
└── INFO.md          # Info del viaggio
```

## Workflow disponibili

- **TravelWorkflow** — pianificazione completa viaggio (ricerca + itinerario + shot list + piano riprese)
- **ContentPipelineWorkflow** — dal materiale grezzo al contenuto approvato (Reel, YouTube, TikTok)
- **SponsorshipWorkflow** — outreach brand, gestione deal inbound, report campagne
- **PublishingWorkflow** — calendario pubblicazione cross-platform con ottimizzazione timing

## Modello AI

Tutti gli agenti usano `claude-opus-4-7` con adaptive thinking per decisioni strategiche complesse.
