from funciones import *
import argparse


def main():
    """Principal Program"""

    # Options #
    parser = argparse.ArgumentParser(
                description='Automatic import virtual machine RHEV',
                prog='import_vm', usage='%(prog)s [options]')
    parser.add_argument('-m', '--manager', metavar='rhevm.i-t-m.local',
                        help='FQDN Manager RHEV', required=True)
    parser.add_argument('-n', '--name', metavar='VM01',
                        help='Name of virtual machine', required=True)
    parser.add_argument('-u', '--user', metavar='admin@internal',
                        help='username with admin privileges DEFAULT=admin',
                        default='admin@internal')
    parser.add_argument('-p', '--password', metavar='p4ssw0rd',
                        help='password for the user', required=True)
    parser.add_argument('-x', '--export', metavar='Exports',
                        help='Name of Export Domain', required=True)
    parser.add_argument('-d', '--storage', metavar='Data',
                        help='Name of Data Domain', required=True)
    parser.add_argument('-c', '--cluster', metavar='CLUS01',
                        help='Name of Cluster', required=True)
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1')
    args = parser.parse_args()
    # Mandatory Params #
    server = args.manager
    username = args.user
    password = args.password
    rhevm_url = "https://%s" % (server)
    # DATOS PARA IMPORT #
    vm_name = args.name
    export_name = args.export
    storage_name = args.storage
    cluster_name = args.cluster

    api = connect(rhevm_url, username, password)

    export = api.storagedomains.get(export_name)
    storage_domain = api.storagedomains.get(storage_name)
    cluster = api.clusters.get(name=cluster_name)

    try:
        export.vms.get(vm_name).import_vm(
            params.Action(storage_domain=storage_domain, cluster=cluster))
        while api.vms.get(vm_name).status.state != 'down':
            sleep(1)
        api.vms.get(vm_name).start()
    except Exception as e:
        print("Failed to import VM:\n%s") % str(e)
    api.disconnect()

if __name__ == '__main__':
    main()