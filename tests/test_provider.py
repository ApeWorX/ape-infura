import os
from unittest.mock import patch

import pytest
import websocket  # type: ignore
from ape.utils import ZERO_ADDRESS

from ape_infura.provider import _WEBSOCKET_CAPABLE_ECOSYSTEMS, Infura, MissingProjectKeyError


def test_infura_http(provider):
    ecosystem = provider.network.ecosystem.name
    network = provider.network.name
    assert isinstance(provider, Infura)
    assert provider.http_uri.startswith("https")
    assert provider.get_balance(ZERO_ADDRESS) > 0
    assert provider.get_block(0)
    ecosystem_uri = "" if ecosystem == "ethereum" else f"{ecosystem}-"
    assert f"https://{ecosystem_uri}{network}.infura.io/v3/" in provider.uri


def test_infura_ws(provider):
    ecosystem = provider.network.ecosystem.name
    if ecosystem not in _WEBSOCKET_CAPABLE_ECOSYSTEMS:
        assert provider.ws_uri is None
        return

    assert provider.ws_uri.startswith("wss")

    try:
        ws = websocket.WebSocket()
        ws.connect(provider.ws_uri)
        ws.close()

    except Exception as err:
        pytest.fail(f"Websocket URI not accessible. Reason: {err}")


def test_load_multiple_api_keys(provider):
    with patch.dict(
        os.environ,
        {"WEB3_INFURA_PROJECT_ID": "key1,key2,key3", "WEB3_INFURA_API_KEY": "key4,key5,key6"},
    ):
        provider.load_api_keys()
        # As there will be API keys in the ENV as well
        assert len(provider.api_keys) >= 6
        assert "key1" in provider.api_keys
        assert "key6" in provider.api_keys


def test_load_single_and_multiple_api_keys(provider):
    with patch.dict(
        os.environ,
        {
            "WEB3_INFURA_PROJECT_ID": "single_key1",
            "WEB3_INFURA_API_KEY": "single_key2",
        },
    ):
        provider.load_api_keys()
        assert len(provider.api_keys) >= 2
        assert "single_key1" in provider.api_keys
        assert "single_key2" in provider.api_keys


def test_random_api_key_selection(provider):
    with patch.dict(os.environ, {"WEB3_INFURA_PROJECT_ID": "key1,key2,key3,key4,key5"}):
        provider.load_api_keys()
        selected_keys = set()
        for _ in range(50):  # Run multiple times to ensure randomness
            selected_keys.add(provider.get_random_api_key())
        assert len(selected_keys) > 1  # Ensure we're getting different keys


def test_missing_project_key_error_raised():
    provider = Infura()
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(MissingProjectKeyError):
            provider.load_api_keys()
