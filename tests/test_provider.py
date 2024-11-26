import os

import pytest
import websocket  # type: ignore
from ape import networks
from web3.exceptions import ExtraDataLengthError
from web3.middleware import geth_poa_middleware

from ape_infura.provider import _WEBSOCKET_CAPABLE_NETWORKS, Infura, _get_session


def test_infura_http(provider):
    ecosystem = provider.network.ecosystem.name
    network = provider.network.name

    if network in ("opbnb-testnet",):
        pytest.skip("This network is weird and has missing trie node errors")

    assert isinstance(provider, Infura)
    assert provider.http_uri.startswith("https")
    ecosystem_uri = "" if ecosystem == "ethereum" else f"{ecosystem}-"
    if "opbnb" in network:
        expected = (
            "https://opbnb-mainnet.infura.io/v3/"
            if network == "opbnb"
            else f"https://{network}.infura.io/v3/"
        )
    else:
        expected = f"https://{ecosystem_uri}{network}.infura.io/v3/"

    assert expected in provider.uri


def test_infura_ws(provider):
    ecosystem = provider.network.ecosystem.name
    if provider.network.name not in _WEBSOCKET_CAPABLE_NETWORKS.get(ecosystem, []):
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


def test_dynamic_poa_check(mocker):
    real = networks.ethereum.holesky.get_provider("infura")
    mock_web3 = mocker.MagicMock()
    mock_web3.eth.get_block.side_effect = ExtraDataLengthError
    infura = Infura(name=real.name, network=real.network)
    patch = mocker.patch("ape_infura.provider._create_web3")
    patch.return_value = mock_web3
    infura.connect()
    mock_web3.middleware_onion.inject.assert_called_once_with(geth_poa_middleware, layer=0)


def test_api_secret():
    os.environ["WEB3_INFURA_PROJECT_SECRET"] = "123"
    session = _get_session()
    assert session.auth == ("", "123")
    del os.environ["WEB3_INFURA_PROJECT_SECRET"]
