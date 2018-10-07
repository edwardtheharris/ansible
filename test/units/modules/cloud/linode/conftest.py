"""Conftest for linode tests."""
import pytest
from units.modules.utils import set_module_args

set_module_args({'state': 'list'})


@pytest.fixture
def api_key(monkeypatch):
    """Api key fixture."""
    monkeypatch.setenv('LINODE_API_KEY', 'foobar')


@pytest.fixture
def auth(monkeypatch):
    """Auth fixture."""
    def patched_test_echo(dummy):
        return [dummy]
    monkeypatch.setattr('linode.api.Api.test_echo', patched_test_echo)
