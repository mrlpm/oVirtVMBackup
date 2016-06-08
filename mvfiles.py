import os
from ovirtvmbackup import OvirtBackup
import shutil

manage = OvirtBackup('https://rhevm.i-t-m.local', 'lperez@itmlabs.local', 'lab2016.')
manage.connect()

disks = manage.api.vms.get('Web01').disks.list()

pwd = os.path.dirname(os.path.abspath(__file__))

export_path = "/exportdomain/"
disk_id1 = "d16b86a8-0f7b-4777-a4da-22380b1fd386"
disk_id2 = "2f0c7f3b-7a65-439f-a55f-e258057c5b86"

gid_1 = 'cff0f290-44df-42f7-bb1d-6714d76f2644'
gid_2 = 'd3566356-dfff-4d02-b62a-9dca30c7839f'

storage_id = "e412a6d5-8d62-4df5-a71c-352c50287a55/"
vm_id = "696121ff-d098-4b3b-bd23-f357037608b1"
virtual_machine = "Guacamole"
path1 = export_path + storage_id


ids = [vm_id, disk_id2, disk_id1]

"""
for np in paths:
    if not os.path.exists(np):
        try:
            os.makedirs(np)
            print("Path {} created.".format(np))
        except OSError as e:
            print("{}".format(e))
"""

dir_to_copy = list()

for root, directories, filenames in os.walk(os.getcwd()):
    for directory in directories:
        #print(os.path.join(root, directory))
        if directory in ids:
#            print("Directory {} found!".format(vm_id))
#            print(os.path.join(root, directory))
#            print("------------------------------")
            dir_to_copy.append(os.path.join(root,directory))
    for filename in filenames:
        #print(os.path.join(root, filename))
        if filename in ids:
#            print("File {} found print directory !".format(vm_id))
#            print(root)
#            print("------------------------------")
            dir_to_copy.append(root)

vms_path = '/master/vms/'
images_path = '/images/'

def create_dirs(vm_name, export_path):
    try:
        os.makedirs(export_path + vm_name + vms_path)
        os.makedirs(export_path + vm_name + images_path)
    except OSError as e:
        print(e)

create_dirs(virtual_machine, export_path)
destination_dir = export_path + virtual_machine + vms_path
destination_dir_images = export_path + virtual_machine + images_path

print(destination_dir)
print(destination_dir_images)
os.chdir(export_path + storage_id + vms_path)
print(os.listdir(os.getcwd()))
shutil.move(vm_id,destination_dir)
os.chdir(export_path + storage_id + images_path)
shutil.move(gid_1,destination_dir_images)
shutil.move(gid_2,destination_dir_images)

def create_tar():
    for dir_saved in dir_to_copy:
        try:
            import tarfile
            with tarfile.open(export_path + virtual_machine + ".tar", "a") as tar:
                tar.add(dir_saved)
        except OSError as e:
            print(e)