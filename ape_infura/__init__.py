from ape import plugins


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape_infura.provider import Infura
    from ape_infura.utils import NETWORKS

    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Infura


def __getattr__(name: str):
    if name == "NETWORKS":
        from ape_infura.utils import NETWORKS

        return NETWORKS

    import ape_infura.provider as module

    return getattr(module, name)


__all__ = ["NETWORKS"]
