import pytest
from ape import networks

from ape_infura.providers import Infura


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        ("ethereum", "mainnet"),
        ("ethereum", "kovan"),
        ("arbitrum", "mainnet"),
        # Uncomment when network name corrected
        # ("arbitrum", "testnet"),
        ("polygon", "mumbai"),
    ],
)
def test_ethereum_mainnet(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        ecosystem_uri = "" if ecosystem == "ethereum" else f"{ecosystem}-"
        assert f"https://{ecosystem_uri}{network}.infura.io/v3/" in provider.uri
