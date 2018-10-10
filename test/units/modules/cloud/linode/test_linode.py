#!/usr/bin/env python
# pylint: disable=invalid-name
"""Tests for the Ansible Linode.

This is intended to test basic CRUD functionality for the Linode module.
"""
import os
from unittest.mock import MagicMock
import pytest

from ansible.compat.tests.mock import patch
from ansible.modules.cloud.linode import linode
from ansible.modules.cloud.linode.linode import linode_api4
from ansible.module_utils import basic
from units.modules.utils import set_module_args

if not linode_api4:
    pytestmark = pytest.mark.skip(
        'test_linode.py requires the `linode-python` module')


class TestLinodeModule():
    """Test class for Ansible Linode module."""
    client = linode_api4.LinodeClient(os.environ.get('LINODE_TOKEN'))
    module = patch.object(basic, 'AnsibleModule', spec=basic.AnsibleModule)

    def test_create_linode(self):
        """Test function to create a linode."""
        set_module_args({'state': 'list'})
        result = linode.create_linode(self.module, self.client)
        assert result is False

    def test_delete_linode(self):
        """Test ability to remove a linode."""
        pass

    def test_list_linodes(self, instances):
        """Test ability to list linodes."""
        with patch.object(
                linode_api4.linode_client.LinodeGroup, 'instances',
                MagicMock(
                    spec=linode_api4.linode_client.LinodeGroup.instances,
                    return_value=instances)):
            self.client.linode.list_instances = MagicMock(
                spec=linode_api4.paginated_list.PaginatedList,
                return_value=instances)

            linodes = linode.list_linodes(self.client)

        assert isinstance(linodes, dict)
        assert linodes.get('changed') is False
        assert linodes.get('instances') == ['testinstance']
