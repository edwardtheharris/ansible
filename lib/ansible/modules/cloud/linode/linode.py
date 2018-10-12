#!/opt/ansible/bin/python3
"""Linode management module."""

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
import os
from pprint import pprint
import linode_api4
from ansible.module_utils.basic import AnsibleModule

# __metaclass__ = type


def create_linode(module, client):
    """Add a new linode.

    state = present, absent
    """
    new_linode = client.linode.instance_create(
        ltype=module.params.get('linode_type'),
        region=module.params.get('region'),
        image=module.params.get('image'),
        authorized_keys=module.params.get('public_key'),
        label=module.params.get('name'))
    return {'changed': True, 'instances': new_linode}


def list_linodes(client):
    """List instances for the given account.

    state = list
    """
    return {
        'changed': False,
        'instances': [linode.label for linode in client.linode.instances()]
    }


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
    module.log(module.params.get('state'))

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
            'image': {'type': 'str'},
            'linode_id': {'type': 'str'},
            'linode_type': {'type': 'str'},
            'name': {'type': 'str'},
            'passowrd': {'type': 'str'},
            'public_key': {'type': 'str'},
            'region': {'type': 'str'},
            'state': {
                'type': 'str',
                'default': 'present',
                'choices': [
                    'absent', 'active', 'deleted', 'list',
                    'present', 'restarted', 'started', 'stopped']},
            'token': {'type': 'str', 'no_log': True},
        },
    )
    module.debug(module.params.get('state'))
    module.debug(module)
    module.debug(pprint(module.params))

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

    results = manage_linodes(module, client)
    module.exit_json(
        changed=results.get('changed'), instances=results.get('instances'))


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

if __name__ == '__main__':
    main()
