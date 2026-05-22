#!/usr/bin/env python3
"""Entry point principale di TravelVision Agency."""
from __future__ import annotations

import os
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint

load_dotenv()

console = Console()


def print_banner() -> None:
    console.print(Panel.fit(
        "[bold cyan]TravelVision Agency[/bold cyan]\n"
        "[dim]Sistema multi-agente — 100 professionisti AI[/dim]\n"
        "[dim]CEO · COO · CMO · Content · Social · Travel · Sponsorizzazioni · Operations[/dim]",
        border_style="cyan",
    ))


def print_agent_response(agent_name: str, role: str, content: str, thinking: str = "") -> None:
    if thinking:
        console.print(f"\n[dim italic]💭 {agent_name} sta ragionando...[/dim italic]")

    console.print(Panel(
        content,
        title=f"[bold green]{agent_name}[/bold green] [dim]— {role}[/dim]",
        border_style="green",
        padding=(1, 2),
    ))


def demo_onboarding(agency) -> None:
    """Demo: onboarding di un nuovo creator."""
    console.print("\n[bold yellow]DEMO: Onboarding Nuovo Creator[/bold yellow]")

    results = agency.onboard_creator(
        creator_name="Lorenzo Viaggio",
        niche="viaggi avventura e destinazioni off-the-beaten-path",
        platforms=["Instagram", "TikTok", "YouTube"],
        monthly_revenue_goal=5000.0,
        target_audience={
            "età": "25-35",
            "interessi": ["viaggi", "avventura", "fotografia", "budget travel"],
            "genere": "mixed",
            "geografia": "Italia e diaspora italiana",
        },
    )

    print_agent_response(
        "Marco Ferretti", "CEO",
        results["ceo_strategy"].content,
        results["ceo_strategy"].thinking,
    )
    print_agent_response(
        "Luca Marino", "CMO",
        results["brand_identity"].content,
        results["brand_identity"].thinking,
    )


def demo_trip_planning(agency) -> None:
    """Demo: pianificazione viaggio di contenuto."""
    console.print("\n[bold yellow]DEMO: Pianificazione Viaggio — Marocco[/bold yellow]")

    plan = agency.plan_content_trip(
        creator_name="Lorenzo Viaggio",
        destination="Marocco",
        start_date="2026-06-15",
        duration_days=7,
        budget=3000.0,
        platforms=["Instagram", "TikTok", "YouTube"],
        content_goals=[
            "Esplorare medine e souk nascosti",
            "Documentare il contrasto tra tradizione e modernità",
            "Produrre contenuti per sponsorizzazione zaini Osprey",
        ],
    )

    if plan.research:
        print_agent_response(
            "Isabella Colombo", "Ricercatore Destinazioni",
            plan.research.content,
            plan.research.thinking,
        )
    if plan.travel_plan:
        print_agent_response(
            "Roberto Zanetti", "Direttore Viaggi",
            plan.travel_plan.content,
            plan.travel_plan.thinking,
        )

    console.print(f"\n[green]✓ Cartella viaggio creata: {plan.folder_path}[/green]")


def demo_content_production(agency) -> None:
    """Demo: produzione contenuto Instagram Reel."""
    console.print("\n[bold yellow]DEMO: Produzione Reel Instagram — Marocco[/bold yellow]")

    trips = agency.list_trips("Lorenzo Viaggio")
    trip_id = trips[0].trip_id if trips else "2026-06-15_marocco"

    package = agency.produce_content_package(
        trip_id=trip_id,
        destination="Marocco, Marrakech",
        platform="Instagram",
        raw_content_description=(
            "Clip del suk El Fna al tramonto, riprese del cuoco che prepara tajine, "
            "drone sulla medina, close-up spezie colorate, golden hour sul palazzo El Badi"
        ),
        creator_style="cinematico, caldi toni dorati, narrazione in prima persona",
        brand_voice="autentico, curioso, mai patinato",
    )

    if package.edit_plan:
        print_agent_response(
            "Davide Conti", "Video Editor",
            package.edit_plan.content,
            package.edit_plan.thinking,
        )
    if package.captions:
        print_agent_response(
            "Valentina De Luca", "Copywriter",
            package.captions.content,
        )


def demo_sponsorship(agency) -> None:
    """Demo: gestione sponsorizzazione."""
    console.print("\n[bold yellow]DEMO: Outreach Brand — Osprey Zaini[/bold yellow]")

    deal = agency.manage_sponsorship(
        creator_profile={
            "nome": "Lorenzo Viaggio",
            "nicchia": "travel avventura",
            "piattaforme": ["Instagram", "TikTok", "YouTube"],
            "follower_ig": 45000,
            "follower_tiktok": 89000,
            "demographics": {"età_media": "28", "interessi": ["outdoor", "zaini", "zaini da trekking"]},
        },
        brand="Osprey",
        collaboration_type="integrazione organica durante viaggio in Marocco + 1 Reel dedicato",
        mode="outreach",
    )

    if deal.pitch:
        print_agent_response(
            "Federico Lombardi", "Senior Copywriter",
            deal.pitch.content,
        )


def demo_owner_review(agency) -> None:
    """Demo: ciclo di revisione del proprietario — 6 settimane."""
    console.print("\n[bold yellow]DEMO: Revisione Settimanale — Vittorio Ferrante (Proprietario)[/bold yellow]")
    console.print("[dim]Il proprietario valuta le performance ogni settimana. Target: +10% su TUTTE le metriche.[/dim]\n")

    # Metriche di partenza — settimana 1 come baseline
    weekly_metrics = [
        # Settimana 1 — baseline
        {
            "follower_instagram": 10000,
            "follower_tiktok": 25000,
            "follower_youtube": 5000,
            "engagement_rate": 3.2,
            "reach": 45000,
            "impressioni": 120000,
            "conversioni": 85,
        },
        # Settimana 2 — crescita insufficiente (sotto +10%)
        {
            "follower_instagram": 10400,
            "follower_tiktok": 26200,
            "follower_youtube": 5200,
            "engagement_rate": 3.3,
            "reach": 47000,
            "impressioni": 124000,
            "conversioni": 88,
        },
        # Settimana 3 — target raggiunto
        {
            "follower_instagram": 11500,
            "follower_tiktok": 28900,
            "follower_youtube": 5750,
            "engagement_rate": 3.7,
            "reach": 52000,
            "impressioni": 138000,
            "conversioni": 97,
        },
        # Settimana 4 — ottimi risultati
        {
            "follower_instagram": 12800,
            "follower_tiktok": 32000,
            "follower_youtube": 6400,
            "engagement_rate": 4.1,
            "reach": 58000,
            "impressioni": 154000,
            "conversioni": 108,
        },
        # Settimana 5 — crescita stagnante
        {
            "follower_instagram": 13100,
            "follower_tiktok": 32800,
            "follower_youtube": 6550,
            "engagement_rate": 4.2,
            "reach": 59500,
            "impressioni": 157000,
            "conversioni": 110,
        },
        # Settimana 6 — recupero finale
        {
            "follower_instagram": 14500,
            "follower_tiktok": 36200,
            "follower_youtube": 7250,
            "engagement_rate": 4.7,
            "reach": 66000,
            "impressioni": 175000,
            "conversioni": 122,
        },
    ]

    deliverables = [
        "5 Reel Instagram, 4 TikTok, 1 video YouTube — viaggio Marocco",
        "6 Reel Instagram, 5 TikTok, 1 YouTube — contenuti Bali",
        "7 Reel Instagram, 6 TikTok, 2 YouTube — Portogallo + 1 collaborazione Osprey",
        "8 Reel Instagram, 7 TikTok, 2 YouTube — Islanda, viral TikTok 2M views",
        "6 Reel Instagram, 5 TikTok, 1 YouTube — contenuti Giappone",
        "9 Reel Instagram, 8 TikTok, 3 YouTube — Giappone + campagna Samsonite",
    ]

    summary = agency.run_owner_review(weekly_metrics, deliverables)

    table = Table(title="Riepilogo 6 Settimane", show_header=True, header_style="bold cyan")
    table.add_column("Settimana", justify="center")
    table.add_column("Esito", justify="center")
    table.add_column("Rework", justify="center")
    table.add_column("Pagamento", justify="right")

    for r in summary["risultati_settimanali"]:
        esito = "[green]✅ Approvata[/green]" if r["approvata"] else "[red]❌ Rifiutata[/red]"
        pag = f"[green]€{r['pagamento']:,.0f}[/green]" if r["pagamento"] > 0 else "[red]€0[/red]"
        table.add_row(str(r["settimana"]), esito, str(r["rework_effettuati"]), pag)

    console.print(table)
    console.print(f"\n  Dovuto:     [bold]€{summary['totale_dovuto']:,.2f}[/bold]")
    console.print(f"  Pagato:     [bold green]€{summary['totale_pagato']:,.2f}[/bold green]")
    console.print(f"  Trattenuto: [bold red]€{summary['totale_trattenuto']:,.2f}[/bold red]")


def show_agency_status(agency) -> None:
    """Mostra lo status dell'agenzia."""
    status = agency.get_agency_status()

    table = Table(title="TravelVision Agency — Team", show_header=True, header_style="bold cyan")
    table.add_column("Dipartimento", style="bold")
    table.add_column("Agenti")

    for dept, agents in status["agenti_attivi"].items():
        table.add_row(dept.title(), "\n".join(agents))

    console.print(table)
    console.print(f"\n[dim]Viaggi registrati: {status['viaggi_registrati']}[/dim]")


def interactive_menu(agency) -> None:
    """Menu interattivo principale."""
    while True:
        console.print("\n[bold]Cosa vuoi fare?[/bold]")
        console.print("  1. Onboarding nuovo creator")
        console.print("  2. Pianificare un viaggio di contenuto")
        console.print("  3. Produrre contenuto per una piattaforma")
        console.print("  4. Gestire una sponsorizzazione")
        console.print("  5. Lista viaggi registrati")
        console.print("  6. Status agenzia")
        console.print("  7. Demo completa")
        console.print("  8. Revisione proprietario (6 settimane)")
        console.print("  0. Esci")

        choice = Prompt.ask("\nScelta", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"])

        if choice == "0":
            console.print("[dim]Arrivederci![/dim]")
            break
        elif choice == "1":
            demo_onboarding(agency)
        elif choice == "2":
            demo_trip_planning(agency)
        elif choice == "3":
            demo_content_production(agency)
        elif choice == "4":
            demo_sponsorship(agency)
        elif choice == "5":
            trips = agency.list_trips()
            if trips:
                for t in trips:
                    console.print(f"  [cyan]{t.trip_id}[/cyan] — {t.name} ({t.creator_name})")
            else:
                console.print("[dim]Nessun viaggio registrato.[/dim]")
        elif choice == "6":
            show_agency_status(agency)
        elif choice == "7":
            demo_onboarding(agency)
            demo_trip_planning(agency)
            demo_content_production(agency)
            demo_sponsorship(agency)
        elif choice == "8":
            demo_owner_review(agency)


def main() -> None:
    print_banner()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Errore: ANTHROPIC_API_KEY non configurata.[/red]")
        console.print("Copia .env.example in .env e inserisci la tua API key.")
        sys.exit(1)

    from agency.orchestrator import TravelVisionAgency
    agency = TravelVisionAgency(api_key=api_key)

    console.print("[green]✓ TravelVision Agency inizializzata.[/green]")
    show_agency_status(agency)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "demo":
            demo_onboarding(agency)
            demo_trip_planning(agency)
            demo_content_production(agency)
            demo_sponsorship(agency)
        elif cmd == "trip" and len(sys.argv) >= 4:
            creator = sys.argv[2]
            destination = sys.argv[3]
            agency.plan_content_trip(
                creator_name=creator,
                destination=destination,
                start_date="2026-07-01",
                duration_days=5,
                budget=2000.0,
                platforms=["Instagram", "TikTok"],
            )
        elif cmd == "review":
            demo_owner_review(agency)
        else:
            console.print(f"[yellow]Comando sconosciuto: {cmd}[/yellow]")
            console.print("Uso: python main.py [demo | trip <creator> <destinazione> | review]")
    else:
        interactive_menu(agency)


if __name__ == "__main__":
    main()
