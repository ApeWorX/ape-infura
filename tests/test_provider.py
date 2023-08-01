import pytest
from ape import networks
from ape.utils import ZERO_ADDRESS

from ape_infura.provider import Infura


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        ("ethereum", "mainnet"),
        ("ethereum", "goerli"),
        ("ethereum", "sepolia"),
        ("arbitrum", "mainnet"),
        ("arbitrum", "goerli"),
        ("optimism", "mainnet"),
        ("optimism", "goerli"),
        ("polygon", "mainnet"),
        ("polygon", "mumbai"),
        ("linea", "mainnet"),
        ("linea", "goerli"),
    ],
)
def test_infura(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance(ZERO_ADDRESS) > 0
        assert provider.get_block(0)
        ecosystem_uri = "" if ecosystem == "ethereum" else f"{ecosystem}-"
        assert f"https://{ecosystem_uri}{network}.infura.io/v3/" in provider.uri
