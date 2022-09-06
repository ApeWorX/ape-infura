from ape import networks

from ape_infura.providers import Infura


def test_provider_works():
    with networks.ethereum.mainnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert provider.uri.startswith(f"https://mainnet.infura.io/v3/")

    with networks.arbitrum.mainnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert provider.uri.startswith(f"https://arbitrum-mainnet.infura.io/v3/")

    with networks.arbitrum.testnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert provider.uri.startswith(f"https://arbitrum-rinkeby.infura.io/v3/")

    with networks.optimism.mainnet.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert provider.uri.startswith(f"https://optimism-mainnet.infura.io/v3/")

    with networks.polygon.mumbai.use_provider("infura") as provider:
        assert isinstance(provider, Infura)
        assert provider.get_balance("0x0000000000000000000000000000000000000000") > 0
        assert provider.uri.startswith(f"https://polygon-mumbai.infura.io/v3/")
