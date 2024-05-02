import ape
import pytest

from ape_infura import NETWORKS


@pytest.fixture
def accounts():
    return ape.accounts


@pytest.fixture
def Contract():
    return ape.Contract


@pytest.fixture
def networks():
    return ape.networks


# NOTE: Using a `str` as param for better pytest test-case name generation.
@pytest.fixture(params=[f"{e}:{n}" for e, values in NETWORKS.items() for n in values])
def provider(networks, request):
    ecosystem, network = request.param.split(":")
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("infura") as provider:
        yield provider
