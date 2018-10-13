#!/usr/bin/env python
# pylint: disable=invalid-name
"""Tests for the Ansible Linode.

This is intended to test basic CRUD functionality for the Linode module.
"""
import pytest

from ansible.modules.cloud.linode import linode
from units.modules.utils import set_module_args

if not linode.linode_api4:
    pytestmark = pytest.mark.skip(
        'test_linode.py requires the `linode-python` module')


def test_create_linode(module, linode_client):
    """Test function to create a linode."""
    set_module_args({'state': 'present'})
    new_linode = linode.create_linode(module, linode_client)

    assert isinstance(new_linode, dict)
    assert new_linode.get('instances')[0].get('id') == 8675309
    assert new_linode.get('instances')[0].get('name') == 'eight.six.seven'


def test_remove_linode(module, linode_client):
    """Test ability to remove a linode."""
    module.params.update({'state': 'absent', 'id': 8675309})
    del_linode = linode_client.linode.instances(
        linode.linode_api4.Instance.id == module.params.get('id'))[0]

    result = linode.remove_linode(module, linode_client)

    assert del_linode.id == 8675309
    assert result.get('changed') is True
    assert result.get('instances')[0].get('id') == 8675309


def test_list_linodes(module, linode_client):
    """Test ability to list linodes."""
    set_module_args({'state': 'list'})
    linodes = linode.list_linodes(module, linode_client)

    assert isinstance(linodes, dict)
    assert linodes.get('changed') is False
    assert linodes.get('instances') == ['the-new-generation']
