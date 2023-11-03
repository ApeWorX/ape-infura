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
