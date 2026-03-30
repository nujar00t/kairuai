"""
Unit tests for KairuAI shared utilities.
"""

import pytest
from agents.utils import truncate_texts, format_price, retry


class TestTruncateTexts:
    def test_empty_input(self):
        assert truncate_texts([]) == []

    def test_fits_within_budget(self):
        texts = ["hello", "world"]
        result = truncate_texts(texts, max_chars=100)
        assert result == texts

    def test_truncates_over_budget(self):
        texts = ["a" * 100, "b" * 100, "c" * 100]
        result = truncate_texts(texts, max_chars=150)
        assert len(result) == 1
        assert result[0] == "a" * 100

    def test_exact_budget(self):
        texts = ["abc", "def"]
        result = truncate_texts(texts, max_chars=6)
        assert result == ["abc", "def"]


class TestFormatPrice:
    def test_large_price(self):
        assert format_price(50000.0) == "$50,000.00"

    def test_mid_price(self):
        result = format_price(142.5)
        assert result == "$142.5000"

    def test_small_price(self):
        result = format_price(0.00001234)
        assert "0.00001234" in result

    def test_one_dollar(self):
        result = format_price(1.0)
        assert result == "$1.0000"


class TestRetry:
    def test_succeeds_first_try(self):
        calls = []

        @retry(max_attempts=3)
        def fn():
            calls.append(1)
            return "ok"

        result = fn()
        assert result == "ok"
        assert len(calls) == 1

    def test_retries_on_failure(self):
        calls = []

        @retry(max_attempts=3, delay=0)
        def fn():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("not yet")
            return "ok"

        result = fn()
        assert result == "ok"
        assert len(calls) == 3

    def test_raises_after_max_attempts(self):
        @retry(max_attempts=2, delay=0)
        def fn():
            raise RuntimeError("always fails")

        with pytest.raises(RuntimeError):
            fn()
