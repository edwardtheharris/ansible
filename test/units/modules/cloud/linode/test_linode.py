#!/usr/bin/env python
# pylint: disable=invalid-name
"""Tests for the Ansible Linode.

This is intended to test basic CRUD functionality for the Linode module.
"""
import os
import pytest
import linode_api4

from ansible.modules.cloud.linode import linode
# from units.modules.utils import set_module_args

if not linode.HAS_LINODE:
    pytestmark = pytest.mark.skip('test_linode.py requires the `linode-python` module')


class TestLinodeModule():
    """Test class for Ansible Linode module."""
    client = linode_api4.LinodeClient(os.environ.get('LINODE_TOKEN'))

    def test_create_linode():
        """Test function to create a linode."""
        pass


    def test_delete_linode():
        """Test ability to remove a linode."""
        pass


    def test_list_linodes(self):
        """Test ability to list linodes."""
        linodes = linode.list_linodes(self.client)

        assert isinstance(linodes, list) 
