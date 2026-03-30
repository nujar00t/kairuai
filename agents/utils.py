"""
KairuAI · Shared utilities for agents.
"""

from __future__ import annotations

import time
import functools
from typing import Callable, Any
from rich.console import Console

console = Console()


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator: retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts:
                        console.print(
                            f"[dim]Retry {attempt}/{max_attempts} for {func.__name__}: {e}[/dim]"
                        )
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]
        return wrapper
    return decorator


def truncate_texts(texts: list[str], max_chars: int = 4000) -> list[str]:
    """Truncate a list of texts to stay within a character budget."""
    result: list[str] = []
    total = 0
    for text in texts:
        if total + len(text) > max_chars:
            break
        result.append(text)
        total += len(text)
    return result


def format_price(value: float) -> str:
    """Format a price value for display."""
    if value >= 1_000:
        return f"${value:,.2f}"
    if value >= 1:
        return f"${value:.4f}"
    return f"${value:.8f}"
