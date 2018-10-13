"""Conftest for linode tests."""
# pylint: disable=protected-access
from unittest import mock
import pytest
from units.modules.utils import set_module_args
from ansible.modules.cloud.linode.linode import linode_api4
from ansible.module_utils.basic import AnsibleModule

PL = linode_api4.paginated_list.PaginatedList
INS = linode_api4.objects.Instance
set_module_args({'state': 'list'})


@pytest.fixture
def linode_client():
    """Return a mocked LinodeClient."""
    client = linode_api4.LinodeClient('')
    linode_api4.objects.Instance.delete = mock.MagicMock(
        linode_api4.objects.Instance, 'delete',
        autospec=True, return_value=True)
    instance = linode_api4.objects.Instance.make_instance(
        8675309, client)
    instance.label = 'eight.six.seven'
    client.linode.instances = mock.Mock(
        client.linode.instances,
        return_value=PL.make_paginated_list(
            {"data": [
                {'id': instance.id,
                 'label': 'the-new-generation'}],
             'pages': 1, 'results': 1},
            client, INS))
    client.linode.instance_create = mock.Mock(
        client.linode.instance_create,
        return_value=(instance, 'rootpwd'))
    return client


@pytest.fixture
def module():
    """Return a hopefully useful module."""
    return AnsibleModule(
        argument_spec={
            "authorized_keys": {'type': 'list'},
            "authorized_users": {'type': 'list'},
            "backups_enabled": {'type': 'bool'},
            "backup_id": {'type': 'int'},
            'booted': {'type': 'bool'},
            "group": {'type': 'str'},
            'image': {'type': 'str'},
            'id': {'type': 'str'},
            'type': {'type': 'str'},
            'name': {'type': 'str'},
            "private_ip": {'type': 'bool'},
            'public_key': {'type': 'str'},
            'region': {'type': 'str'},
            'root_pass': {'type': 'str', 'no_log': True},
            "stackscript_id": {'type': 'int'},
            "stackscript_data": {'type': 'str'},
            'state': {
                'type': 'str',
                'default': 'present',
                'choices': [
                    'absent', 'active', 'deleted', 'list',
                    'present', 'restarted', 'started', 'stopped']},
            "swap_size": {'type': 'int'},
            'tags': {'type': 'list'},
            'token': {'type': 'str', 'no_log': True},
        },
    )


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
