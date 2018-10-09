#!/opt/ansible/bin/python3
"""Linode management module."""
# pylint: disable=invalid-name,wrong-import-position

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
import os
import linode_api4
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


def create_linode(module, client):
    """Add a new linode.

    state = present, absent
    """
    return {'module': module, 'client': client}


def list_linodes(client):
    """List instances for the given account.

    state = list
    """
    return [i.label for i in client.linode.instances()]


def manage_linodes(module, client):
    """Function for management of Linodes.

    :param module: The current module.
    :param client: Linode API client.
    """
    manage_functions = {
        'absent': remove_linode(module, client),
        'list': list_linodes(client),
        'present': create_linode(module, client),
        'started': start_linode(module, client),
        'stopped': stop_linode(module, client)
    }

    return manage_functions.get(module.params.get('state'))


def remove_linode(module, client):
    """Remove an existing linode."""
    return {'module': module, 'client': client}


def start_linode(module, client):
    """Start a given linode."""
    return {'module': module, 'client': client}


def stop_linode(module, client):
    """Stop a given Linode."""
    return {'module': module, 'client': client}


def main():
    """Main module execution."""
    module = AnsibleModule(
        argument_spec={
            'state': {
                'type': 'str',
                'default': 'present',
                'choices': [
                    'absent', 'active', 'deleted', 'list',
                    'present', 'restarted', 'started', 'stopped']},
            'token': {'type': 'str', 'no_log': True},
            'name': {'type': 'str'},
        },
    )

    # Setup the api_key
    if not module.params.get('token'):
        try:
            module.params.update({
                'token': os.environ.get('LINODE_TOKEN')})
        except KeyError as exception:
            module.fail_json(msg='Unable to load %s' % exception)

    # setup the auth
    try:
        client = linode_api4.LinodeClient(module.params.get('token'))
    except KeyError as exception:
        module.fail_json(msg='%s' % exception)

    module.exit_json(changed=False, instances=manage_linodes(module, client))


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

if __name__ == '__main__':
    main()
