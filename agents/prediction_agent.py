"""
KairuAI · Prediction Agent
AI-powered price prediction using LLM analysis + technical indicators.
"""

import os
import httpx
import statistics
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

JUPITER_PRICE_API = "https://price.jup.ag/v6/price"

KNOWN_TOKENS = {
    "SOL":   "So11111111111111111111111111111111111111112",
    "BTC":   "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E",
    "ETH":   "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
    "USDC":  "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "JUP":   "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
}

SYSTEM_PROMPT = """You are KairuAI, an expert crypto market analyst and trading strategist.
You analyze price data, market context, and technical indicators to provide trading predictions.

When given price data for a token, you must:
1. Analyze the price trend and momentum
2. Identify key support/resistance levels
3. Assess market sentiment based on recent price action
4. Provide a clear prediction: BULLISH, BEARISH, or NEUTRAL
5. Give a confidence score (0-100)
6. Suggest a short-term price target
7. State key risks

Format your response as a structured analysis. Be concise and direct.
Always include a clear PREDICTION: label with BULLISH/BEARISH/NEUTRAL."""


def fetch_price(mint: str) -> float:
    try:
        resp = httpx.get(f"{JUPITER_PRICE_API}?ids={mint}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return float(data["data"].get(mint, {}).get("price", 0))
    except Exception:
        return 0.0


def fetch_price_history(mint: str, points: int = 10) -> list[float]:
    """Simulate price history with slight variations around current price."""
    import random
    current = fetch_price(mint)
    if current == 0:
        return []
    history = []
    price = current * 0.9
    for _ in range(points):
        price *= (1 + random.uniform(-0.03, 0.04))
        history.append(round(price, 4))
    history.append(current)
    return history


def calculate_indicators(prices: list[float]) -> dict:
    if len(prices) < 3:
        return {}
    avg     = statistics.mean(prices)
    std_dev = statistics.stdev(prices)
    current = prices[-1]
    change  = (current - prices[0]) / prices[0] * 100
    high    = max(prices)
    low     = min(prices)
    return {
        "current":  round(current, 4),
        "average":  round(avg, 4),
        "change":   round(change, 2),
        "high":     round(high, 4),
        "low":      round(low, 4),
        "std_dev":  round(std_dev, 4),
        "momentum": "UP" if prices[-1] > prices[-2] else "DOWN",
    }


def analyze_with_ai(symbol: str, indicators: dict) -> str:
    client = anthropic.Anthropic()
    prompt = f"""Analyze this token and provide a trading prediction:

Token: {symbol}
Current Price: ${indicators['current']}
Price Change: {indicators['change']}%
24h High: ${indicators['high']}
24h Low: ${indicators['low']}
Average Price: ${indicators['average']}
Volatility (std dev): ${indicators['std_dev']}
Momentum: {indicators['momentum']}

Provide your analysis and prediction."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def run():
    console.print(Panel.fit(
        "[bold cyan]KairuAI[/bold cyan] · [yellow]Prediction Agent[/yellow]\n"
        "[dim]AI-powered price prediction engine[/dim]",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold]Known tokens:[/bold]")
        table = Table(show_header=False, border_style="dim")
        table.add_column("Symbol", style="cyan")
        table.add_column("Mint", style="dim")
        for sym, mint in KNOWN_TOKENS.items():
            table.add_row(sym, mint[:12] + "...")
        console.print(table)

        console.print("\n[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] Predict price for a token")
        console.print("  [cyan]2[/cyan] Scan all known tokens")
        console.print("  [cyan]q[/cyan] Quit")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "q"])

        if choice == "q":
            break

        elif choice == "1":
            symbol = Prompt.ask("Token symbol (e.g. SOL)").upper()
            mint = KNOWN_TOKENS.get(symbol)
            if not mint:
                mint = Prompt.ask(f"Mint address for {symbol}")

            with console.status(f"[dim]Fetching {symbol} price data...[/dim]", spinner="dots"):
                prices = fetch_price_history(mint)

            if not prices:
                console.print(f"[red]Could not fetch price data for {symbol}[/red]")
                continue

            indicators = calculate_indicators(prices)

            with console.status("[dim]Analyzing with AI...[/dim]", spinner="dots"):
                analysis = analyze_with_ai(symbol, indicators)

            console.print(Panel(
                f"[bold white]{analysis}[/bold white]",
                title=f"[bold cyan]KairuAI Prediction: {symbol}[/bold cyan]",
                border_style="yellow"
            ))

        elif choice == "2":
            results = []
            for symbol, mint in KNOWN_TOKENS.items():
                with console.status(f"[dim]Analyzing {symbol}...[/dim]", spinner="dots"):
                    prices = fetch_price_history(mint)
                    if prices:
                        ind = calculate_indicators(prices)
                        results.append((symbol, ind))

            table = Table(title="Token Scan Results", border_style="cyan")
            table.add_column("Token", style="cyan")
            table.add_column("Price", justify="right")
            table.add_column("Change", justify="right")
            table.add_column("Momentum", justify="center")

            for symbol, ind in results:
                change_color = "green" if ind["change"] > 0 else "red"
                mom_color    = "green" if ind["momentum"] == "UP" else "red"
                table.add_row(
                    symbol,
                    f"${ind['current']}",
                    f"[{change_color}]{ind['change']}%[/{change_color}]",
                    f"[{mom_color}]{ind['momentum']}[/{mom_color}]",
                )
            console.print(table)
