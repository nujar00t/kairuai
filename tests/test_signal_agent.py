"""
Unit tests for KairuAI Signal Agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from agents.signal_agent import fetch_tweets, fetch_news_sentiment, analyze_sentiment


class TestFetchTweets:
    @patch("agents.signal_agent._twitter_client")
    def test_returns_list_of_strings(self, mock_client_fn):
        mock_client = MagicMock()
        mock_tweet1 = MagicMock()
        mock_tweet1.text = "SOL is pumping!"
        mock_tweet2 = MagicMock()
        mock_tweet2.text = "Bullish on Solana ecosystem"
        mock_client.search_recent_tweets.return_value = MagicMock(data=[mock_tweet1, mock_tweet2])
        mock_client_fn.return_value = mock_client

        result = fetch_tweets("SOL", limit=10)
        assert isinstance(result, list)
        assert all(isinstance(t, str) for t in result)

    @patch("agents.signal_agent._twitter_client")
    def test_returns_empty_on_no_data(self, mock_client_fn):
        mock_client = MagicMock()
        mock_client.search_recent_tweets.return_value = MagicMock(data=None)
        mock_client_fn.return_value = mock_client

        result = fetch_tweets("UNKNOWN_TOKEN_XYZ")
        assert result == []

    @patch("agents.signal_agent._twitter_client")
    def test_returns_empty_on_exception(self, mock_client_fn):
        mock_client_fn.side_effect = Exception("API error")
        result = fetch_tweets("SOL")
        assert result == []


class TestFetchNewsSentiment:
    @patch("httpx.get")
    def test_returns_list(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = """
        <html><body>
        <h3>Solana hits new high</h3>
        <h4>SOL ecosystem grows</h4>
        </body></html>
        """
        mock_get.return_value = mock_resp
        result = fetch_news_sentiment("SOL")
        assert isinstance(result, list)

    @patch("httpx.get")
    def test_returns_empty_on_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        result = fetch_news_sentiment("SOL")
        assert result == []


class TestAnalyzeSentiment:
    def test_returns_no_data_message_on_empty(self):
        result = analyze_sentiment("SOL", [])
        assert "No data" in result

    @patch("agents.signal_agent.anthropic.Anthropic")
    def test_calls_anthropic_with_texts(self, mock_anthropic_cls):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="BULLISH · BUY · Confidence: 80")]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_cls.return_value = mock_client

        result = analyze_sentiment("SOL", ["SOL is mooning", "Bullish on SOL"])
        assert isinstance(result, str)
        assert len(result) > 0
        mock_client.messages.create.assert_called_once()
