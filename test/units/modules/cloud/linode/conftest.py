"""Conftest for linode tests."""
import pickle
import pytest
from units.modules.utils import set_module_args

set_module_args({'state': 'list'})


@pytest.fixture
def instances():
    """Return PaginatedList."""
    lpfile = open('test/units/modules/cloud/linode/linode_list.out', 'rb')
    return_value = pickle.load(lpfile)
    lpfile.close()
    return return_value


@pytest.fixture
def api_key(monkeypatch):
    """Api key fixture."""
    monkeypatch.setenv('LINODE_TOKEN', 'foobar')


@pytest.fixture
def auth(monkeypatch):
    """Auth fixture."""
    def patched_test_echo(dummy):
        return [dummy]
    monkeypatch.setattr('linode.api.Api.test_echo', patched_test_echo)
