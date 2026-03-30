"""
Unit tests for KairuAI Prediction Agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.prediction_agent import (
    calculate_indicators,
    fetch_price_history,
    KNOWN_TOKENS,
)


class TestCalculateIndicators:
    def test_returns_empty_for_short_list(self):
        assert calculate_indicators([]) == {}
        assert calculate_indicators([100.0]) == {}
        assert calculate_indicators([100.0, 101.0]) == {}

    def test_basic_indicators(self):
        prices = [100.0, 102.0, 98.0, 105.0, 110.0]
        result = calculate_indicators(prices)

        assert "current" in result
        assert "average" in result
        assert "change" in result
        assert "high" in result
        assert "low" in result
        assert "std_dev" in result
        assert "momentum" in result

    def test_current_is_last_price(self):
        prices = [100.0, 102.0, 98.0, 105.0, 110.0]
        result = calculate_indicators(prices)
        assert result["current"] == 110.0

    def test_high_low(self):
        prices = [100.0, 102.0, 98.0, 105.0, 110.0]
        result = calculate_indicators(prices)
        assert result["high"] == 110.0
        assert result["low"] == 98.0

    def test_momentum_up(self):
        prices = [100.0, 102.0, 104.0]
        result = calculate_indicators(prices)
        assert result["momentum"] == "UP"

    def test_momentum_down(self):
        prices = [104.0, 102.0, 100.0]
        result = calculate_indicators(prices)
        assert result["momentum"] == "DOWN"

    def test_change_positive(self):
        prices = [100.0, 105.0, 110.0]
        result = calculate_indicators(prices)
        assert result["change"] == 10.0

    def test_change_negative(self):
        prices = [110.0, 105.0, 100.0]
        result = calculate_indicators(prices)
        assert round(result["change"], 2) == round((100.0 - 110.0) / 110.0 * 100, 2)


class TestKnownTokens:
    def test_known_tokens_exist(self):
        assert "SOL" in KNOWN_TOKENS
        assert "BTC" in KNOWN_TOKENS
        assert "ETH" in KNOWN_TOKENS
        assert "USDC" in KNOWN_TOKENS

    def test_mint_addresses_are_strings(self):
        for symbol, mint in KNOWN_TOKENS.items():
            assert isinstance(mint, str), f"{symbol} mint should be a string"
            assert len(mint) > 10, f"{symbol} mint address too short"


class TestFetchPriceHistory:
    @patch("agents.prediction_agent.fetch_price")
    def test_returns_list(self, mock_fetch):
        mock_fetch.return_value = 142.5
        result = fetch_price_history("fake_mint", points=5)
        assert isinstance(result, list)

    @patch("agents.prediction_agent.fetch_price")
    def test_returns_empty_on_zero_price(self, mock_fetch):
        mock_fetch.return_value = 0.0
        result = fetch_price_history("fake_mint")
        assert result == []

    @patch("agents.prediction_agent.fetch_price")
    def test_last_element_is_current_price(self, mock_fetch):
        mock_fetch.return_value = 100.0
        result = fetch_price_history("fake_mint", points=5)
        assert result[-1] == 100.0
