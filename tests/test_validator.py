import importlib

import datascout.validator as validator


def test_is_safe_url_blocks_unlisted_hosts(monkeypatch):
    monkeypatch.setenv("ALLOWED_DOWNLOAD_HOSTS", "example.com,docs.example.org")
    importlib.reload(validator)

    assert validator.is_safe_url("https://example.com/data.csv") is True
    assert validator.is_safe_url("https://docs.example.org/file.json") is True
    assert validator.is_safe_url("https://evil.example.net/data.csv") is False
    assert validator.is_safe_url("http://example.com/data.csv") is False
