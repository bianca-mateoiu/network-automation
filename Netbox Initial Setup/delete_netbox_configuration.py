import sys
import os
sys.path.append(os.path.abspath("/home/jcluser/network_automation/Netbox Initial Setup"))
from Netbox_REST_APIs import *

delete_ip_addresses()

delete_interface_connections()

delete_devices()

delete_prefixes()

delete_sites()

delete_device_types()

delete_tenants()

delete_device_role()

delete_prefix_roles()

delete_platforms()
