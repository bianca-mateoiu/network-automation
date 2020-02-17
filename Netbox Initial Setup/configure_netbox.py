
import sys
import os
sys.path.append(os.path.abspath("/home/jcluser/network_automation/Netbox Initial Setup"))
from Netbox_REST_APIs import *


create_device_roles()

create_tenants()

create_sites()

create_manufacturers()

create_device_types("vMX", "juniper")

create_device_types("Nexus", "cisco")

create_interface_templates('vMX')

create_interface_templates('Nexus')

create_prefix_roles()

for item in my_variables_in_yaml['prefix_roles']:
   get_prefix_role_id(item)

create_prefixes()


create_platform()

create_devices()

create_ip_addresses('legaturi_centrale')
create_ip_addresses('legaturi_pe_cpe')
create_ip_addresses('adresare_management')

enable_management_ip_address()

#create_interface_connections()
