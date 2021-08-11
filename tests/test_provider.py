from ape import networks

from ape_infura.providers import Infura


def test_provider_works():
    with networks.ethereum.mainnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
