from ape import plugins

from .providers import Infura

NETWORKS = {
    "ethereum": [
        "mainnet",
        "ropsten",
        "rinkeby",
        "kovan",
        "goerli",
    ],
    "arbitrum": [
        "mainnet",
        "tesnet",
    ],
    "optimism": [
        "mainnet",
        "kovan",
        "goerli",
    ],
    "polygon": [
        "mainnet",
        "mumbai",
    ],
}


@plugins.register(plugins.ProviderPlugin)
def providers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura
