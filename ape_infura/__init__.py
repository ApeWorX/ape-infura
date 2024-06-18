from ape import plugins

from .provider import Infura

NETWORKS = {
    "arbitrum": [
        "mainnet",
        "sepolia",
    ],
    "avalanche": [
        "fuji",
        "mainnet",
    ],
    "blast": [
        "mainnet",
        "sepolia",
    ],
    "ethereum": [
        "mainnet",
        "sepolia",
    ],
    # TODO: Comment out after ape-linea supports 0.7
    # "linea": [
    #     "mainnet",
    # ],
    "optimism": [
        "mainnet",
        "sepolia",
    ],
    "polygon": [
        "mainnet",
        "amoy",
    ],
}


@plugins.register(plugins.ProviderPlugin)
def providers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura
