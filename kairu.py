#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║          K A I R U   A I                 ║
║   Autonomous AI Trading Agent            ║
║   $KAIRUAI · Built on Solana             ║
╚══════════════════════════════════════════╝
"""

import os
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

load_dotenv()
console = Console()

BANNER = """[bold cyan]
██╗  ██╗ █████╗ ██╗██████╗ ██╗   ██╗     █████╗ ██╗
██║ ██╔╝██╔══██╗██║██╔══██╗██║   ██║    ██╔══██╗██║
█████╔╝ ███████║██║██████╔╝██║   ██║    ███████║██║
██╔═██╗ ██╔══██║██║██╔══██╗██║   ██║    ██╔══██║██║
██║  ██╗██║  ██║██║██║  ██║╚██████╔╝    ██║  ██║██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝
[/bold cyan]
[dim]Autonomous AI Trading Agent · [bold]$KAIRUAI[/bold] · Built on Solana[/dim]"""


def show_banner():
    console.print(BANNER)


def show_menu():
    table = Table(show_header=False, border_style="dim", padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=6)
    table.add_column("Agent", style="bold white")
    table.add_column("Description", style="dim")

    table.add_row("1", "Prediction Agent", "AI price prediction via LLM + technical analysis")
    table.add_row("2", "Signal Agent",     "Sentiment analysis from Twitter + news → signals")
    table.add_row("3", "Trading Agent",    "Execute swaps on Solana via Jupiter (Node.js)")
    table.add_row("4", "Polymarket Agent", "Prediction market intelligence (Node.js)")
    table.add_row("q", "Quit",             "Exit KairuAI")

    console.print(Panel(table, title="[bold cyan]Select Agent[/bold cyan]", border_style="cyan"))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """KairuAI — Autonomous AI Trading Agent · $KAIRUAI"""
    if ctx.invoked_subcommand is None:
        show_banner()
        while True:
            show_menu()
            choice = Prompt.ask(
                "\n[bold cyan]kairu[/bold cyan]",
                choices=["1", "2", "3", "4", "q"]
            )
            if choice == "q":
                console.print("\n[dim]KairuAI shutting down.[/dim]")
                break
            elif choice == "1":
                from agents.prediction_agent import run
                run()
            elif choice == "2":
                from agents.signal_agent import run
                run()
            elif choice == "3":
                console.print("\n[dim]Run: cd agents/trading && npm run dev[/dim]")
            elif choice == "4":
                console.print("\n[dim]Run: cd agents/polymarket && npm run dev[/dim]")


@cli.command()
def predict():
    """Launch Prediction Agent — AI price forecasting"""
    show_banner()
    from agents.prediction_agent import run
    run()


@cli.command()
def signal():
    """Launch Signal Agent — sentiment analysis → trading signals"""
    show_banner()
    from agents.signal_agent import run
    run()


@cli.command()
def trading():
    """Launch Trading Agent — Solana DEX swaps via Jupiter"""
    show_banner()
    console.print(Panel(
        "[dim]TypeScript agent. Run:[/dim]\n\n"
        "  cd agents/trading\n"
        "  npm install\n"
        "  npm run dev",
        title="[bold cyan]Trading Agent[/bold cyan]",
        border_style="cyan"
    ))


@cli.command()
def polymarket():
    """Launch Polymarket Agent — prediction market intelligence"""
    show_banner()
    console.print(Panel(
        "[dim]TypeScript agent. Run:[/dim]\n\n"
        "  cd agents/polymarket\n"
        "  npm install\n"
        "  npm run dev",
        title="[bold cyan]Polymarket Agent[/bold cyan]",
        border_style="cyan"
    ))


if __name__ == "__main__":
    cli()
