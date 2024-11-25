from ape import plugins


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape_infura.provider import Infura
    from ape_infura.utils import NETWORKS

    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura


def __getattr__(name: str):
    if name == "Infura":
        from ape_infura.provider import Infura

        return Infura

    elif name == "NETWORKS":
        from ape_infura.utils import NETWORKS

        return NETWORKS

    else:
        raise AttributeError(name)


__all__ = [
    "Infura",
    "NETWORKS",
]
