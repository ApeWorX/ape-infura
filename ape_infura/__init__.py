from ape import plugins

from .provider import Infura

NETWORKS = {
    "ethereum": [
        "mainnet",
        "goerli",
        "sepolia",
    ],
    "arbitrum": [
        "mainnet",
        "goerli",
        "sepolia",
    ],
    "optimism": [
        "mainnet",
        "goerli",
        "sepolia",
    ],
    "polygon": [
        "mainnet",
        "mumbai",
    ],
    "linea": [
        "mainnet",
        "goerli",
    ],
}


@plugins.register(plugins.ProviderPlugin)
def providers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura
