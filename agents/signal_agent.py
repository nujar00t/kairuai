"""
KairuAI · Signal Agent
Sentiment analysis from Twitter/X + news → trading signals.
"""

import os
import httpx
import anthropic
import tweepy
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

SYSTEM_PROMPT = """You are KairuAI's signal analyzer. You receive social media posts and news
about crypto tokens and generate trading signals based on sentiment.

Analyze the content and output:
1. Overall sentiment: BULLISH / BEARISH / NEUTRAL
2. Confidence score: 0-100
3. Key themes detected (e.g. hype, FUD, whale activity, partnership, exploit)
4. Signal: BUY / SELL / HOLD
5. Brief reasoning (2-3 sentences max)

Be concise and data-driven."""


def _twitter_client() -> tweepy.Client:
    return tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        wait_on_rate_limit=True,
    )


def fetch_tweets(query: str, limit: int = 20) -> list[str]:
    if not os.getenv("TWITTER_BEARER_TOKEN"):
        console.print(
            "[yellow]⚠ TWITTER_BEARER_TOKEN not set — skipping Twitter, using news only.[/yellow]"
        )
        return []
    try:
        client = _twitter_client()
        results = client.search_recent_tweets(
            query=f"{query} -is:retweet lang:en",
            max_results=min(limit, 100),
            tweet_fields=["text", "public_metrics"]
        )
        if not results.data:
            return []
        return [t.text for t in results.data]
    except Exception as e:
        console.print(f"[yellow]Twitter fetch failed: {e}[/yellow]")
        return []


def fetch_news_sentiment(token: str) -> list[str]:
    """Scrape crypto news headlines for a token."""
    try:
        url = f"https://cryptonews.com/search/?q={token}"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; KairuAI/1.0)"}
        resp = httpx.get(url, headers=headers, timeout=10)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        headlines = [h.get_text(strip=True) for h in soup.select("h3, h4, .title")[:15]]
        return headlines
    except Exception:
        return []


def analyze_sentiment(token: str, texts: list[str]) -> str:
    if not texts:
        return "No data available for sentiment analysis."

    client = anthropic.Anthropic()
    combined = "\n".join(f"- {t}" for t in texts[:20])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Token: {token}\n\nSocial/news data:\n{combined}"
        }]
    )
    return response.content[0].text


def run():
    console.print(Panel.fit(
        "[bold cyan]KairuAI[/bold cyan] · [magenta]Signal Agent[/magenta]\n"
        "[dim]Sentiment analysis → trading signals[/dim]",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("  [cyan]1[/cyan] Analyze sentiment for a token (Twitter + news)")
        console.print("  [cyan]2[/cyan] Quick news scan")
        console.print("  [cyan]q[/cyan] Quit")

        choice = Prompt.ask("\nChoose", choices=["1", "2", "q"])

        if choice == "q":
            break

        elif choice == "1":
            token = Prompt.ask("Token name or ticker (e.g. Solana, $SOL)")

            with console.status("[dim]Fetching Twitter data...[/dim]", spinner="dots"):
                tweets = fetch_tweets(token, limit=20)

            with console.status("[dim]Fetching news...[/dim]", spinner="dots"):
                news = fetch_news_sentiment(token)

            all_data = tweets + news
            console.print(f"[dim]Collected {len(tweets)} tweets + {len(news)} headlines[/dim]")

            with console.status("[dim]Analyzing sentiment with AI...[/dim]", spinner="dots"):
                signal = analyze_sentiment(token, all_data)

            console.print(Panel(
                f"[bold white]{signal}[/bold white]",
                title=f"[bold cyan]Signal: {token}[/bold cyan]",
                border_style="magenta"
            ))

        elif choice == "2":
            token = Prompt.ask("Token to scan news for")
            with console.status("[dim]Fetching news...[/dim]", spinner="dots"):
                headlines = fetch_news_sentiment(token)

            if not headlines:
                console.print("[dim]No headlines found.[/dim]")
            else:
                console.print(f"\n[bold]Headlines for {token}:[/bold]")
                for h in headlines:
                    if h:
                        console.print(f"  [dim]•[/dim] {h}")
