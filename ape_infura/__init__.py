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
        "sepolia",
    ],
    "optimism": [
        "mainnet",
        "sepolia",
    ],
    "polygon": [
        "mainnet",
        "mumbai",
        "amoy",
    ],
    "blast": [
        "mainnet",
        "sepolia",
    ],
    # TODO: Comment out after ape-linea supports 0.7
    # "linea": [
    #     "mainnet",
    #     "goerli",
    # ],
}


@plugins.register(plugins.ProviderPlugin)
def providers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura
