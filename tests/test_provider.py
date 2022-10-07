import pytest
from ape import networks
from requests import HTTPError

from ape_infura.providers import Infura


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        ("ethereum", "mainnet"),
        ("ethereum", "goerli"),
        ("arbitrum", "mainnet"),
        ("optimism", "mainnet"),
        ("polygon", "mumbai"),
    ],
)
def test_infura(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("infura") as provider:
        assert isinstance(provider, Infura)

        try:
            balance = provider.get_balance("0x0000000000000000000000000000000000000000")
        except HTTPError as err:
            if err.response.status_code == 403:
                pytest.skip("Please set proper API key.")
                return

            raise

        assert balance > 0
        ecosystem_uri = "" if ecosystem == "ethereum" else f"{ecosystem}-"
        assert f"https://{ecosystem_uri}{network}.infura.io/v3/" in provider.uri
