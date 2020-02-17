
###########################################################
# Acest script este folosit pentru actualizarea fisierelor
# cu date din Netbox pentru un singur host
###########################################################

################################################################
# folosire: python ansible_update_host_var_file.py $device_name
################################################################

import sys
import os
import fnmatch
import ipaddress
sys.path.append(os.path.abspath("/home/jcluser/network_automation/Netbox Initial Setup"))
from Netbox_REST_APIs import *

device = sys.argv[1] if len(sys.argv) == 2 else sys.exit("Trebuie sa introduceti un singur host!")

if not os.path.exists("/home/jcluser/network_automation/host_vars"):
    os.mkdir("/home/jcluser/network_automation/host_vars")

device_id=get_device_id(device)
url=url_base + 'api/dcim/devices/' + str(device_id)
rest_call = requests.get(url, headers=headers)
item=rest_call.json()

host_var={'role':[str(item['device_role']['name'])]}
host_var["dns_servers"]=[str(item['custom_fields']['dns_servers'])]
host_var["ntp_servers"]=[str(item['custom_fields']['ntp_servers'])]

url_int=url_base + 'api/ipam/ip-addresses/?device=' + item['name']
rest_call_int = requests.get(url_int, headers=headers)

interface={}
core_links=[]
pe_cpe_links=[]
cpe_pe_link_name=''
cpe_pe_link_LAN=[]

for int in rest_call_int.json()['results']:
    name=str(int['interface']['name'])

    interface[name]={ 'ipv4': str(int['address']).split("/")[0],
                                                    'ipv4_mask' : str(int['address']).split("/")[1],
                                                     'description': str(int['description'])
                                                     }

       # daca host-ul este CPE si are PE in descriere
    if ( "pe-" in int['description'] and "CPE" in str(item['device_role']['name'])):
         cpe_pe_link_name=str(int['description']).split("catre")[1].strip()

     # daca host-ul este CPE si are LAN in descriere
    if ( "LAN" in int['description'] and "CPE" in str(item['device_role']['name'])):
         cpe_pe_link_LAN.append(str(int['address']))

       # daca host-ul este PE si are PE in descriere
    if ( " pe-" in int['description'] and str(item['device_role']['name']).startswith("PE") ):
         core_links.append(str(int['description']).split("catre")[1].strip())

       # daca host-ul este PE si are CPE in descriere
    if ( "cpe" in int['description'] and str(item['device_role']['name']).startswith("PE") ):
         pe_cpe_links.append(str(int['description']).split("catre")[1].strip())

host_var['interfaces']=interface

if cpe_pe_link_name:
     host_var["cpe_pe_link"]={cpe_pe_link_name:cpe_pe_link_LAN}
if core_links:
     host_var["core_links"]=core_links
if pe_cpe_links:
     host_var["pe_cpe_links"]=pe_cpe_links

with open('/home/jcluser/network_automation/host_vars/'+item['name'], 'w+') as file:
               yaml.dump(host_var, file)


#################### generarea legaturilor PE-CPE  ####################


for cpe_file in os.listdir('/home/jcluser/network_automation/host_vars/'):
    if fnmatch.fnmatch(cpe_file, 'cpe*'):
        with open('/home/jcluser/network_automation/host_vars/' + cpe_file, 'r+') as f_cpe:
            cpe = yaml.load(f_cpe)
            if ("cpe_pe_link" in cpe.keys()):
                for pe in cpe["cpe_pe_link"]:
                    with open('/home/jcluser/network_automation/host_vars/' + pe, 'r+') as f_pe:
                        p_pe = yaml.load(f_pe)
                        if ("pe_cpe_links" in p_pe.keys()):
                            for p_cpe in p_pe["pe_cpe_links"]:
                                if (p_cpe==cpe_file):
                                    p_pe["pe_cpe_links"]={p_cpe:cpe["cpe_pe_link"][pe]}
                                    with open('/home/jcluser/network_automation/host_vars/'+pe, 'w+') as new_pe_file:
                                        yaml.dump(p_pe, new_pe_file)
