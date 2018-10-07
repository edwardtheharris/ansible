#!/usr/bin/env python
# pylint: disable=invalid-name
"""Tests for the Ansible Linode module."""
import pytest

from ansible.modules.cloud.linode import linode
from units.modules.utils import set_module_args

if not linode.HAS_LINODE:
    pytestmark = pytest.mark.skip('test_linode.py requires the `linode-python` module')


def test_create_linode():
    """Test function to create a linode."""
    pass
