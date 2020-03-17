import sys
import os
sys.path.append(os.path.abspath("/home/jcluser/network_automation/Netbox Initial Setup"))
from Netbox_REST_APIs import *


#create_ip_addresses('core_links')
#create_ip_addresses('pe_cpe')
create_ip_addresses('LAN')
create_ip_addresses('management')
