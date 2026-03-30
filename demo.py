#!/usr/bin/env python3
"""
KairuAI · Demo Script
Simulates agent output for recording — no API keys required.
"""

import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich import box

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


def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(msg, duration=2.0):
    with Progress(
        SpinnerColumn(),
        TextColumn("[dim]{task.description}[/dim]"),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(msg, total=None)
        time.sleep(duration)


def demo_prediction():
    console.print(Panel.fit(
        "[bold cyan]KairuAI[/bold cyan] · [yellow]Prediction Agent[/yellow]\n"
        "[dim]AI-powered price prediction engine[/dim]",
        border_style="cyan"
    ))
    time.sleep(0.5)

    console.print("\n[bold]Token:[/bold] [cyan]SOL[/cyan]")
    time.sleep(0.3)

    spinner("Fetching SOL price data...", 1.8)
    spinner("Analyzing with Claude AI...", 2.2)

    analysis = """[bold green]PREDICTION: BULLISH[/bold green]
[dim]────────────────────────────────────[/dim]
[white]Confidence:[/white]     [bold yellow]81/100[/bold yellow]
[white]Current Price:[/white]  [bold]$143.20[/bold]
[white]Price Target:[/white]   [bold green]$162.00[/bold green]  [dim](+13.1%)[/dim]
[white]Momentum:[/white]       [bold green]↑ UP[/bold green]
[white]24h Change:[/white]     [bold green]+4.7%[/bold green]

[dim]Analysis:[/dim]
SOL shows strong upward momentum with price holding above
key support at $138. Validator activity is up 12% WoW and
ecosystem TVL is expanding. RSI at 61 — room to run before
overbought territory. Watch $148 resistance as next target.

[dim]Key risk:[/dim] Broader market correction or BTC weakness."""

    console.print(Panel(
        analysis,
        title="[bold cyan]KairuAI Prediction: SOL[/bold cyan]",
        border_style="yellow",
        box=box.ROUNDED,
    ))
    time.sleep(1.0)


def demo_signal():
    console.print(Panel.fit(
        "[bold cyan]KairuAI[/bold cyan] · [magenta]Signal Agent[/magenta]\n"
        "[dim]Sentiment analysis → trading signals[/dim]",
        border_style="cyan"
    ))
    time.sleep(0.5)

    console.print("\n[bold]Token:[/bold] [cyan]$SOL[/cyan]")
    time.sleep(0.3)

    spinner("Fetching Twitter/X data...", 1.5)
    console.print("[dim]  Collected 20 tweets + 8 headlines[/dim]")
    time.sleep(0.3)
    spinner("Analyzing sentiment with Claude AI...", 2.0)

    signal = """[bold green]Sentiment: BULLISH[/bold green]
[dim]────────────────────────────────────[/dim]
[white]Signal:[/white]      [bold green]BUY[/bold green]
[white]Confidence:[/white]  [bold yellow]74/100[/bold yellow]

[white]Key themes detected:[/white]
  [cyan]•[/cyan] Ecosystem growth  [cyan]•[/cyan] Validator activity
  [cyan]•[/cyan] Developer inflow  [cyan]•[/cyan] Institutional interest

[dim]Reasoning:[/dim]
Twitter sentiment is predominantly positive with high-engagement
posts around Solana ecosystem growth. News flow shows 3 bullish
catalysts in last 24h. No significant FUD or whale sell signals
detected. Sentiment score: 7.4/10."""

    console.print(Panel(
        signal,
        title="[bold cyan]Signal: $SOL[/bold cyan]",
        border_style="magenta",
        box=box.ROUNDED,
    ))
    time.sleep(1.0)


def demo_scan():
    console.print("\n[bold]Running full token scan...[/bold]\n")
    time.sleep(0.3)

    tokens = ["SOL", "BTC", "ETH", "JUP", "USDC"]
    for token in tokens:
        spinner(f"Analyzing {token}...", 0.8)

    table = Table(
        title="[bold]Token Scan Results[/bold]",
        border_style="cyan",
        box=box.ROUNDED,
    )
    table.add_column("Token", style="bold cyan", width=8)
    table.add_column("Price", justify="right", width=12)
    table.add_column("24h Change", justify="right", width=12)
    table.add_column("Momentum", justify="center", width=10)
    table.add_column("Signal", justify="center", width=8)

    rows = [
        ("SOL",  "$143.20", "[green]+4.7%[/green]",  "[green]↑ UP[/green]",   "[bold green]BUY[/bold green]"),
        ("BTC",  "$67,420", "[green]+1.2%[/green]",  "[green]↑ UP[/green]",   "[bold green]BUY[/bold green]"),
        ("ETH",  "$3,280",  "[red]-0.8%[/red]",      "[red]↓ DOWN[/red]",     "[yellow]HOLD[/yellow]"),
        ("JUP",  "$1.24",   "[green]+8.3%[/green]",  "[green]↑ UP[/green]",   "[bold green]BUY[/bold green]"),
        ("USDC", "$1.00",   "[dim]0.0%[/dim]",       "[dim]— FLAT[/dim]",     "[dim]HOLD[/dim]"),
    ]

    for row in rows:
        table.add_row(*row)
        time.sleep(0.15)

    console.print(table)
    time.sleep(0.8)


def main():
    console.clear()
    console.print(BANNER)
    time.sleep(1.0)

    console.print("\n[dim]Starting demo — Prediction Agent[/dim]\n")
    time.sleep(0.8)
    demo_prediction()

    time.sleep(0.5)
    console.print("\n[dim]Starting demo — Signal Agent[/dim]\n")
    time.sleep(0.8)
    demo_signal()

    time.sleep(0.5)
    demo_scan()

    console.print(Panel.fit(
        "[bold cyan]github.com/nujar00t/kairuai[/bold cyan]\n"
        "[dim]⭐ Star if this was useful[/dim]",
        border_style="dim"
    ))
    time.sleep(0.5)


if __name__ == "__main__":
    main()
