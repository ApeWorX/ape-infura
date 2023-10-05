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


@pytest.fixture(params=[(name, net) for name, values in NETWORKS.items() for net in values])
def provider(networks, request):
    ecosystem_cls = networks.get_ecosystem(request.param[0])
    network_cls = ecosystem_cls.get_network(request.param[1])
    with network_cls.use_provider("infura") as provider:
        yield provider
