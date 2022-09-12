import pytest
from ape import networks

from ape_infura.providers import Infura


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        ("ethereum", "mainnet"),
        ("ethereum", "kovan"),
        ("arbitrum", "mainnet"),
        ("polygon", "mumbai"),
    ],
)
def test_provider(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert f"https://{ecosystem}-{network}.infura.io/v3/" in provider.uri


@pytest.mark.parametrize("network", "mainnet", "kovan")
def test_ethereum(networks, network):
    network = networks.ethereum.get_network(networks)
    with network.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert f"https://{network}.infura.io/v3/" in provider.uri


def test_arbitrum_testnet():
    with networks.arbitrum.testnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert f"https://arbitrum-rinkeby.infura.io/v3/" in provider.uri
