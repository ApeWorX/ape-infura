import os

import pytest
import websocket  # type: ignore
from ape.utils import ZERO_ADDRESS

from ape_infura.provider import _WEBSOCKET_CAPABLE_ECOSYSTEMS, Infura


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


def test_load_multiple_api_keys(provider, mocker):
    original_env = os.environ.copy()
    mocker.patch.dict(
        os.environ,
        {"WEB3_INFURA_PROJECT_ID": "key1,key2,key3", "WEB3_INFURA_API_KEY": "key4,key5,key6"},
    )
    # As there will be API keys in the ENV as well
    provider.disconnect()
    assert len(provider._api_keys) == 6
    assert "key1" in provider._api_keys
    assert "key6" in provider._api_keys

    os.environ.clear()
    os.environ.update(original_env)

    # Disconnect so key isn't cached.
    provider.disconnect()


def test_load_single_and_multiple_api_keys(provider, mocker):
    original_env = os.environ.copy()
    mocker.patch.dict(
        os.environ,
        {
            "WEB3_INFURA_PROJECT_ID": "single_key1",
            "WEB3_INFURA_API_KEY": "single_key2",
        },
    )
    provider.disconnect()
    assert len(provider._api_keys) == 2
    assert "single_key1" in provider._api_keys
    assert "single_key2" in provider._api_keys

    os.environ.clear()
    os.environ.update(original_env)

    # Disconnect so key isn't cached.
    provider.disconnect()


def test_uri_with_random_api_key(provider, mocker):
    original_env = os.environ.copy()
    mocker.patch.dict(os.environ, {"WEB3_INFURA_PROJECT_ID": "key1, key2, key3, key4, key5, key6"})

    uris = set()
    for _ in range(100):  # Generate multiple URIs
        provider.disconnect()  # connect to a new URI
        uri = provider.uri
        uris.add(uri)
        assert uri.startswith("https")
        assert "/v3" in uri
    assert len(uris) > 1  # Ensure we're getting different URIs with different

    os.environ.clear()
    os.environ.update(original_env)

    # Disconnect so key isn't cached.
    provider.disconnect()
