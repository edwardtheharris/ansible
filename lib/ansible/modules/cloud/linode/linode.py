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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


def randompass():
    '''
    Generate a long random password that comply to Linode requirements
    '''
    # Linode API currently requires the following:
    # It must contain at least two of these four character classes:
    # lower case letters - upper case letters - numbers - punctuation
    # we play it safe :)
    import random
    import string
    # as of python 2.4, this reseeds the PRNG from urandom
    random.seed()
    lower = ''.join(random.choice(
        string.ascii_lowercase) for x in list(range(6)))
    upper = ''.join(random.choice(
        string.ascii_uppercase) for x in list(range(6)))
    number = ''.join(random.choice(string.digits) for x in list(range(6)))
    punct = ''.join(random.choice(string.punctuation) for x in list(range(6)))
    p = lower + upper + number + punct
    return ''.join(random.sample(p, len(p)))


def check_linode(module, client):
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
        'absent': check_linode(module, client),
        'list': list_linodes(client),
        'present': check_linode(module, client),
        'started': start_linode(module, client),
        'stopped': stop_linode(module, client)
    }

    return manage_functions.get(module.params.get('state'))


def start_linode(module, client):
    """Start a given linode."""
    return {'module': module, 'client': client}


def stop_linode(module, client):
    """Stop a given Linode."""
    return {'module': module, 'client': client}


def getInstanceDetails(api, server):
    '''
    Return the details of an instance, populating IPs, etc.
    '''
    instance = {'id': server['LINODEID'],
                'name': server['LABEL'],
                'public': [],
                'private': []}

    # Populate with ips
    for ip in api.linode_ip_list(LinodeId=server['LINODEID']):
        if ip['ISPUBLIC'] and 'ipv4' not in instance:
            instance['ipv4'] = ip['IPADDRESS']
            instance['fqdn'] = ip['RDNS_NAME']
        if ip['ISPUBLIC']:
            instance['public'].append({'ipv4': ip['IPADDRESS'],
                                       'fqdn': ip['RDNS_NAME'],
                                       'ip_id': ip['IPADDRESSID']})
        else:
            instance['private'].append({'ipv4': ip['IPADDRESS'],
                                        'fqdn': ip['RDNS_NAME'],
                                        'ip_id': ip['IPADDRESSID']})
    return instance

    """
    # See if we can match an existing
    server details with the provided linode_id
    if linode_id:
        # For the moment we only consider linode_id as criteria for match
        # Later we can use more (size, name, etc.) and update existing
        servers = client.linode_list(LinodeId=linode_id)
        # Attempt to fetch details about disks and configs only if servers are
        # found with linode_id
        if servers:
            disks = client.linode_disk_list(LinodeId=linode_id)
            configs = client.linode_config_list(LinodeId=linode_id)

    """
    """
    # Act on the state
    if state in ('active', 'present', 'started'):

        # Multi step process/validation:
        #  - need linode_id (entity)
        #  - need disk_id for linode_id - create disk from distrib
        #  - need config_id for linode_id - create config (need kernel)

        # Any create step triggers a job that need to be waited for.
        if not servers:
            for arg in (name, plan, distribution, datacenter):
                if not arg:
                    module.fail_json(
                        msg='%s is required for %s state' % (arg, state))
            # Create linode entity
            new_server = True

            # Get size of all individually listed
            disks to subtract from Distribution disk
            used_disk_space = 0
            if additional_disks is None else sum(disk['Size']
            for disk in additional_disks)

            try:
                res = client.linode_create(
                    DatacenterID=datacenter, PlanID=plan,
                                        PaymentTerm=payment_term)
                linode_id = res['LinodeID']
                # Update linode Label to match name
                client.linode_update(LinodeId=linode_id,
                    Label='%s-%s' % (linode_id, name))
                # Update Linode with Ansible configuration options
                client.linode_update(LinodeId=linode_id,
                LPM_DISPLAYGROUP=displaygroup, WATCHDOG=watchdog, **kwargs)
                # Save server
                servers = client.linode_list(LinodeId=linode_id)
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
    """
    """
        # Add private IP to Linode
        if private_ip:
            try:
                res = client.linode_ip_addprivate(LinodeID=linode_id)
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])

        if not disks:
            for arg in (name, linode_id, distribution):
                if not arg:
                    module.fail_json(msg='%s is
                        required for %s state' % (arg, state))
            # Create disks (1 from distrib, 1 for SWAP)
            new_server = True
            try:
                if not password:
                    # Password is required on
                    creation, if not provided generate one
                    password = randompass()
                if not swap:
                    swap = 512
                # Create data disk
                size = servers[0]['TOTALHD'] - used_disk_space - swap

                if ssh_pub_key:
                    res = client.linode_disk_createfromdistribution(
                        LinodeId=linode_id, DistributionID=distribution,
                        rootPass=password, rootSSHKey=ssh_pub_key,
                        Label='%s data disk (lid: %s)' % (name, linode_id),
                        Size=size)
                else:
                    res = client.linode_disk_createfromdistribution(
                        LinodeId=linode_id, DistributionID=distribution,
                        rootPass=password,
                        Label='%s data disk (lid: %s)' % (name, linode_id),
                        Size=size)
                jobs.append(res['JobID'])
                # Create SWAP disk
                res = client.linode_disk_create(
                    LinodeId=linode_id, Type='swap',
                                             Label='%s swap disk (
                                lid: %s)' % (name, linode_id),
                                             Size=swap)
                # Create individually listed disks at specified size
                if additional_disks:
                    for disk in additional_disks:
                        # If a disk Type is not passed in, default to ext4
                        if disk.get('Type') is None:
                            disk['Type'] = 'ext4'
                        res = client.linode_disk_create(
                            LinodeID=linode_id, Label=disk['Label'],
                            Size=disk['Size'], Type=disk['Type'])

                jobs.append(res['JobID'])
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
    """
    """
        if not configs:
            for arg in (name, linode_id, distribution):
                if not arg:
                    module.fail_json(
                    msg='%s is required for %s state' % (arg, state))

            # Check architecture
            for distrib in client.avail_distributions():
                if distrib['DISTRIBUTIONID'] != distribution:
                    continue
                arch = '32'
                if distrib['IS64BIT']:
                    arch = '64'
                break

            # Get latest kernel matching arch if kernel_id is not specified
            if not kernel_id:
                for kernel in client.avail_kernels():
                    if not kernel['LABEL'].startswith('Latest %s' % arch):
                        continue
                    kernel_id = kernel['KERNELID']
                    break

            # Get disk list
            disks_id = []
            for disk in client.linode_disk_list(LinodeId=linode_id):
                if disk['TYPE'] == 'ext3':
                    disks_id.insert(0, str(disk['DISKID']))
                    continue
                disks_id.append(str(disk['DISKID']))
            # Trick to get the 9 items in the list
            while len(disks_id) < 9:
                disks_id.append('')
            disks_list = ','.join(disks_id)

            # Create config
            new_server = True
            try:
                client.linode_config_create(
                    LinodeId=linode_id, KernelId=kernel_id,
                 Disklist=disks_list, Label='%s config' % name)
                configs = client.linode_config_list(LinodeId=linode_id)
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
    """
    """
        # Start / Ensure servers are running
        for server in servers:
            # Refresh server state
            server = client.linode_list(LinodeId=server['LINODEID'])[0]
            # Ensure existing servers are up and running, boot if necessary
            if server['STATUS'] != 1:
                res = client.linode_boot(LinodeId=linode_id)
                jobs.append(res['JobID'])
                changed = True

            # wait here until the instances are up
            wait_timeout = time.time() + wait_timeout
            while wait and wait_timeout > time.time():
                # refresh the server details
                server = client.linode_list(LinodeId=server['LINODEID'])[0]
                # status:
                #  -2: Boot failed
                #  1: Running
                if server['STATUS'] in (-2, 1):
                    break
                time.sleep(5)
            if wait and wait_timeout <= time.time():
                # waiting took too long
                module.fail_json(
                    msg='Timeout waiting on %s (lid: %s)' %
                        (server['LABEL'], server['LINODEID']))
            # Get a fresh copy of the server details
            server = client.linode_list(LinodeId=server['LINODEID'])[0]
            if server['STATUS'] == -2:
                module.fail_json(msg='%s (lid: %s) failed to boot' %
                                 (server['LABEL'], server['LINODEID']))
            # From now on we know the task is a success
            # Build instance report
            instance = getInstanceDetails(client, server)
            # depending on wait flag select the status
            if wait:
                instance['status'] = 'Running'
            else:
                instance['status'] = 'Starting'

            # Return the root password if this is a new box and no SSH key
            # has been provided
            if new_server and not ssh_pub_key:
                instance['password'] = password
            instances.append(instance)

    elif state in ('stopped'):
        if not linode_id:
            module.fail_json(msg='linode_id is required for stopped state')

        if not servers:
            module.fail_json(msg='Server (lid: %s) not found' % (linode_id))

        for server in servers:
            instance = getInstanceDetails(client, server)
            if server['STATUS'] != 2:
                try:
                    res = client.linode_shutdown(LinodeId=linode_id)
                except Exception as e:
                    module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
                instance['status'] = 'Stopping'
                changed = True
            else:
                instance['status'] = 'Stopped'
            instances.append(instance)

    elif state in ('restarted'):
        if not linode_id:
            module.fail_json(msg='linode_id is required for restarted state')

        if not servers:
            module.fail_json(msg='Server (lid: %s) not found' % (linode_id))

        for server in servers:
            instance = getInstanceDetails(client, server)
            try:
                res = client.linode_reboot(LinodeId=server['LINODEID'])
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
            instance['status'] = 'Restarting'
            changed = True
            instances.append(instance)

    elif state in ('absent', 'deleted'):
        for server in servers:
            instance = getInstanceDetails(client, server)
            try:
                client.linode_delete(
                    LinodeId=server['LINODEID'], skipChecks=True)
            except Exception as e:
                module.fail_json(msg='%s' % e.value[0]['ERRORMESSAGE'])
            instance['status'] = 'Deleting'
            changed = True
            instances.append(instance)

    # Ease parsing if only 1 instance
    if len(instances) == 1:
        module.exit_json(changed=changed, instance=instances[0])

    module.exit_json(changed=changed, instances=instances)
    """


def main():
    """Main module execution."""
    # module.fail_json(msg='linode_client4 required for this module')

    """
    state = module.params.get('state')
    client_key = module.params.get('api_key')
    name = module.params.get('name')
    alert_bwin_enabled = module.params.get('alert_bwin_enabled')
    alert_bwin_threshold = module.params.get('alert_bwin_threshold')
    alert_bwout_enabled = module.params.get('alert_bwout_enabled')
    alert_bwout_threshold = module.params.get('alert_bwout_threshold')
    alert_bwquota_enabled = module.params.get('alert_bwquota_enabled')
    alert_bwquota_threshold = module.params.get('alert_bwquota_threshold')
    alert_cpu_enabled = module.params.get('alert_cpu_enabled')
    alert_cpu_threshold = module.params.get('alert_cpu_threshold')
    alert_diskio_enabled = module.params.get('alert_diskio_enabled')
    alert_diskio_threshold = module.params.get('alert_diskio_threshold')
    backupsenabled = module.params.get('backupsenabled')
    backupweeklyday = module.params.get('backupweeklyday')
    backupwindow = module.params.get('backupwindow')
    displaygroup = module.params.get('displaygroup')
    plan = module.params.get('plan')
    additional_disks = module.params.get('additional_disks')
    distribution = module.params.get('distribution')
    datacenter = module.params.get('datacenter')
    kernel_id = module.params.get('kernel_id')
    linode_id = module.params.get('linode_id')
    payment_term = module.params.get('payment_term')
    password = module.params.get('password')
    private_ip = module.params.get('private_ip')
    ssh_pub_key = module.params.get('ssh_pub_key')
    swap = module.params.get('swap')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    watchdog = int(module.params.get('watchdog'))

    check_items = {
        'alert_bwin_enabled': module.params.get('alert_bwin_enabled'),
        'alert_bwin_threshold': module.params.get('alert_bwin_threshold'),
        'alert_bwout_enabled': module.params.get('alert_bwout_enabled'),
        'alert_bwout_threshold': module.params.get('alert_bwout_threshold'),
        'alert_bwquota_enabled': module.params.get('alert_bwquota_enabled'),
        'alert_bwquota_threshold':
            module.params.get('alert_bwquota_threshold'),
        'alert_cpu_enabled': module.params.get('alert_cpu_enabled'),
        'alert_cpu_threshold': module.params.get('alert_cpu_threshold'),
        'alert_diskio_enabled': module.params.get('alert_diskio_enabled'),
        'alert_diskio_threshold': module.params.get('alert_diskio_threshold'),
        'backupweeklyday': module.params.get('backupweeklyday'),
        'backupwindow': module.params.get('backupwindow'),
    }
    """
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
            # alert_bwin_enabled=dict(type='bool'),
            # alert_bwin_threshold=dict(type='int'),
            # alert_bwout_enabled=dict(type='bool'),
            # alert_bwout_threshold=dict(type='int'),
            # alert_bwquota_enabled=dict(type='bool'),
            # alert_bwquota_threshold=dict(type='int'),
            # alert_cpu_enabled=dict(type='bool'),
            # alert_cpu_threshold=dict(type='int'),
            # alert_diskio_enabled=dict(type='bool'),
            # alert_diskio_threshold=dict(type='int'),
            # backupsenabled=dict(type='int'),
            # backupweeklyday=dict(type='int'),
            # backupwindow=dict(type='int'),
            # displaygroup=dict(type='str', default=''),
            # plan=dict(type='int'),
            # additional_disks=dict(type='list'),
            # distribution=dict(type='int'),
            # datacenter=dict(type='int'),
            # kernel_id=dict(type='int'),
            # linode_id=dict(type='int', aliases=['lid']),
            # payment_term=dict(type='int', default=1, choices=[1, 12, 24]),
            # password=dict(type='str', no_log=True),
            # private_ip=dict(type='bool'),
            # ssh_pub_key=dict(type='str'),
            # swap=dict(type='int', default=512),
            # wait=dict(type='bool', default=True),
            # wait_timeout=dict(default=300),
            # watchdog=dict(type='bool', default=True),
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


if __name__ == '__main__':
    main()
