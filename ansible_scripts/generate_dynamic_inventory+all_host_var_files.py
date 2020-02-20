
#############################################################
# Acest script genereaza inventory-ul pentru Ansible dinamic
# si fisierele host var cu date preluate din Netbox API
#############################################################

####################################################################
# folosire: python generate_dynamic_inventory+all_host_var_files.py
####################################################################

import sys
import os
import fnmatch
import ipaddress
sys.path.append(os.path.abspath("/home/jcluser/network-automation/Netbox Initial Setup"))
from Netbox_REST_APIs import *

#################### generare inventory dinamic ####################

ansible_inventory_file = open('/home/jcluser/network-automation/hosts', "w")

ansible_inventory_file.write("#Ansible dynamic inventory file generated from Netbox API\n")
ansible_inventory_file.write("\n")

url=url_base + 'api/dcim/manufacturers/'

rest_call = requests.get(url, headers=headers)

for item in rest_call.json()['results']:
    manufacturer = item['name']
    ansible_inventory_file.write("######################### "+manufacturer+" #########################\n")
    ansible_inventory_file.write("[" + manufacturer + ":children]\n")

    url=url_base + 'api/dcim/device-types/?is_network_device=True&manufacturer=' + manufacturer

    rest_call = requests.get(url, headers=headers)

    for item in rest_call.json()['results']:
       model = item['model']
       ansible_inventory_file.write(model + "\n")
    ansible_inventory_file.write("\n")

    for item in rest_call.json()['results']:
       model = item['model']
       ansible_inventory_file.write("[" + model+ "]\n")
       device_type_id = get_device_type_id(model)
       url = url_base + 'api/dcim/devices/?manufacturer=' + manufacturer + '&device_type_id=' + str(device_type_id) + '&is_network_device=True&has_primary_ip=True'
       rest_call = requests.get(url, headers=headers)
       for item in rest_call.json()['results']:
           name = item['name']
           ip = item["primary_ip4"]["address"]
           ip = ip.split("/")[0]
           ansible_inventory_file.write(name + " ansible_host=" + ip + "\n")
       ansible_inventory_file.write("\n")

    ansible_inventory_file.write("######################### Per site \n")
    url = url_base + 'api/dcim/sites/'
    rest_call_get_sites = requests.get(url, headers=headers)
    for site in rest_call_get_sites.json()['results']:
        site_name = site['name']
        ansible_inventory_file.write("[" + site_name + "]\n")
        url = url_base + 'api/dcim/devices/?manufacturer=' + manufacturer + '&site=' + site_name + '&is_network_device=True&has_primary_ip=True'
        rest_call_get_devices = requests.get(url, headers=headers)
        for device in rest_call_get_devices.json()['results']:
            device_name = device['name']
            ansible_inventory_file.write(device_name + "\n")
        ansible_inventory_file.write("\n")

    ansible_inventory_file.write("######################### Per role \n")
    url= url_base + 'api/dcim/device-roles/'
    rest_call_get_roles = requests.get(url, headers=headers)
    for role in rest_call_get_roles.json()['results']:
        role_name = role['name']
        ansible_inventory_file.write("[" + role_name + "]\n")
        url = url_base + 'api/dcim/devices/?manufacturer=' + manufacturer + '&role=' + role_name + '&is_network_device=True&has_primary_ip=True'
        rest_call_get_devices = requests.get(url, headers=headers)
        for device in rest_call_get_devices.json()['results']:
            device_name = device['name']
            ansible_inventory_file.write(device_name + "\n")
        ansible_inventory_file.write("\n")
ansible_inventory_file.close()

#################### generarea fisierelor HOST VAR ####################

if not os.path.exists("/home/jcluser/network-automation/host_vars"):
    os.mkdir("/home/jcluser/network-automation/host_vars")

url=url_base + 'api/dcim/manufacturers/'
rest_call = requests.get(url, headers=headers)

for item in rest_call.json()['results']:
    manufacturer = item['name']
    url=url_base + 'api/dcim/device-types/?is_network_device=True&manufacturer=' + manufacturer
    rest_call = requests.get(url, headers=headers)

    for item in rest_call.json()['results']:
       model = item['model']
       device_type_id = get_device_type_id(model)
       url = url_base + 'api/dcim/devices/?manufacturer=' + manufacturer + '&device_type_id=' + str(device_type_id) + '&is_network_device=True&has_primary_ip=True'
       rest_call = requests.get(url, headers=headers)

       for item in rest_call.json()['results']:
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
                    cpe_pe_link_name=str(int['description']).split(" to ")[1].strip()

                # daca host-ul este CPE si are LAN in descriere
               if ( "LAN" in int['description'] and "CPE" in str(item['device_role']['name'])):
                    cpe_pe_link_LAN.append(str(int['address']))

                  # daca host-ul este PE si are PE in descriere
               if ( " pe-" in int['description'] and str(item['device_role']['name']).startswith("PE") ):
                    core_links.append(str(int['description']).split(" to ")[1].strip())

                  # daca host-ul este PE si are CPE in descriere
               if ( "cpe" in int['description'] and str(item['device_role']['name']).startswith("PE") ):
                    pe_cpe_links.append(str(int['description']).split(" to ")[1].strip())

           host_var['interfaces']=interface

           if cpe_pe_link_name:
                host_var["cpe_pe_link"]={cpe_pe_link_name:cpe_pe_link_LAN}
           if core_links:
                host_var["core_links"]=core_links
           if pe_cpe_links:
                host_var["pe_cpe_links"]=pe_cpe_links

           with open('/home/jcluser/network-automation/host_vars/'+item['name'], 'w+') as file:
               yaml.dump(host_var, file)


####################  PE-CPE  links ####################


for cpe_file in os.listdir('/home/jcluser/network-automation/host_vars/'):
    if fnmatch.fnmatch(cpe_file, 'cpe*'):
        with open('/home/jcluser/network-automation/host_vars/' + cpe_file, 'r+') as f_cpe:
            cpe = yaml.load(f_cpe)
            if ("cpe_pe_link" in cpe.keys()):
                for pe in cpe["cpe_pe_link"]:
                    with open('/home/jcluser/network-automation/host_vars/' + pe, 'r+') as f_pe:
                        p_pe = yaml.load(f_pe)
                        if ("pe_cpe_links" in p_pe.keys()):
                            for p_cpe in p_pe["pe_cpe_links"]:
                                if (p_cpe==cpe_file):
                                    networks=[]
                                    for ip in cpe["cpe_pe_link"][pe]:
                                        networks.append(str(ipaddress.ip_interface(unicode(ip)).network))
                                    p_pe["pe_cpe_links"]={p_cpe + "_" + str(cpe["role"]):networks}
                                    with open('/home/jcluser/network-automation/host_vars/'+pe, 'w+') as new_pe_file:
                                        yaml.dump(p_pe, new_pe_file)
