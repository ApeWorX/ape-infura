import ape
import pytest


@pytest.fixture
def accounts():
    return ape.accounts


@pytest.fixture
def Contract():
    return ape.Contract


@pytest.fixture
def networks():
    return ape.networks
