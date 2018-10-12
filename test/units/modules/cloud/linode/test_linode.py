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


def test_create_linode(module):
    """Test function to create a linode."""
    assert module is False


def test_delete_linode():
    """Test ability to remove a linode."""
    pass


def test_list_linodes(linode_client):
    """Test ability to list linodes."""
    set_module_args({'state': 'list'})
    linodes = linode.list_linodes(linode_client)
    assert isinstance(linodes, dict)
    assert linodes.get('changed') is False
    assert linodes.get('instances') == ['the-new-generation']
