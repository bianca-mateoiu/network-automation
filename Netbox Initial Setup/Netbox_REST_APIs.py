#######################################################################
# Defining the get, create and delete functions via REST calls
#######################################################################

import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint
import yaml
import time


###############################################################################
#  Creating url_base from variables.yml
###############################################################################

def import_variables_from_file():
 my_variables_file=open('/home/jcluser/network_automation/Netbox Initial Setup/variables.yml', 'r')
 my_variables_in_string=my_variables_file.read()
 my_variables_in_yaml=yaml.load(my_variables_in_string)
 my_variables_file.close()
 return my_variables_in_yaml

my_variables_in_yaml=import_variables_from_file()

url_base = 'http://' + my_variables_in_yaml['ip'] + '/'

token = my_variables_in_yaml['token']

headers={
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

##########################################################
# Get & Create functions
##########################################################

def create_device_roles():
 url=url_base + 'api/dcim/device-roles/'
 for item in my_variables_in_yaml['device-roles']:
     payload={
         "name": item,
         "slug": item,
         "color": "2196f3"
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'device role ' + item + ' successfully created'
     else:
         print 'failed to create device role ' + item

def get_device_role_id(role):
 url=url_base + 'api/dcim/device-roles/?name=' + role
 rest_call = requests.get(url, headers=headers)
 role_id = rest_call.json()['results'][0]['id']
 return role_id

def create_tenants():
 url=url_base + 'api/tenancy/tenants/'
 for item in my_variables_in_yaml['tenants']:
     payload={
         "name": item,
         "slug": item
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'tenant ' + item + ' successfully created'
     else:
         print 'failed to create tenant ' + item

def get_tenant_id(tenant):
 url=url_base + 'api/tenancy/tenants/?name=' + tenant
 rest_call = requests.get(url, headers=headers)
 tenant_id = rest_call.json()['results'][0]['id']
 return tenant_id

def create_manufacturers():
 url=url_base + 'api/dcim/manufacturers/'
 tenant_id=get_tenant_id(my_variables_in_yaml['tenants'][0])
 for item in my_variables_in_yaml['manufacturers']:
     payload={
         "name": item,
         "slug": item,
         "tenant": tenant_id
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'manufacturer ' + item + ' successfully created'
     else:
         print 'failed to create manufacturer ' + item

def get_manufacturer_id(manufacturer):
 url=url_base + 'api/dcim/manufacturers/?name=' + manufacturer
 rest_call = requests.get(url, headers=headers)
 manufacturer_id = rest_call.json()['results'][0]['id']
 return manufacturer_id

def create_platform():
 url=url_base + 'api/dcim/platforms/'
 payload={
     "napalm_driver": "junos",
     'name': 'junos',
     'rpc_client': 'juniper-junos',
     'slug': 'junos'
 }
 rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
 if rest_call.status_code == 201:
     print 'platform junos with a junos napalm_driver successfully created'
 else:
     print 'failed to create platform junos'

def get_platform_id(platform):
 url=url_base + 'api/dcim/platforms/?name=' + platform
 rest_call = requests.get(url, headers=headers)
 platform_id = rest_call.json()['results'][0]['id']
 return platform_id

def create_sites():
 url=url_base + 'api/dcim/sites/'
 tenant_id=get_tenant_id(my_variables_in_yaml['tenants'][0])
 for item in my_variables_in_yaml['sites']:
     payload={
         "name": item,
         "slug": item,
         "tenant": tenant_id
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'site ' + item + ' successfully created'
     else:
         print 'failed to create site ' + item

def get_site_id(site):
 url=url_base + 'api/dcim/sites/?name=' + site
 rest_call = requests.get(url, headers=headers)
 site_id = rest_call.json()['results'][0]['id']
 return site_id

def create_device_types(model, manufacturer):
    url=url_base + 'api/dcim/device-types/'
    manufacturer_id=get_manufacturer_id(manufacturer)
    device_types_list=[{"manufacturer": manufacturer_id, "model": model, "slug": model, "part_number": "650-049938", "u_height": 1, "is_full_depth": True, "is_network_device": True}]
    for item in device_types_list:
        payload={
        "manufacturer": item['manufacturer'],
        "model": item['model'],
        "slug": item['slug'],
        "part_number": item['part_number'],
        "u_height": item['u_height'],
        "is_full_depth": item["is_full_depth"],
        "is_network_device": item["is_network_device"]
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        if rest_call.status_code == 201:
            print 'device type ' + item['model'] + ' successfully created'
        else:
            print 'failed to create device type ' + item['model']

def get_device_type_id(model):
    url=url_base + 'api/dcim/device-types/?model=' + model
    rest_call = requests.get(url, headers=headers)
    device_type_id = rest_call.json()['results'][0]['id']
    return device_type_id

def create_interface_templates(model):
    url=url_base + 'api/dcim/interface-templates/'
    if model == "vMX":
        for item in range (0, 4):
            payload={
                "device_type": get_device_type_id(model),
                "name": "ge-0/0/" + str(item),
                "form_factor": 1200,
                "mgmt_only": False
            }
            rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        payload={
            "device_type": get_device_type_id(model),
            "name": "fxp0",
            "form_factor": 1000,
            "mgmt_only": True
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))

    if model == "Nexus":
        for item in range (0, 6):
            payload={
                "device_type": get_device_type_id(model),
                "name": "Ge0/" + str(item),
                "form_factor": 1200,
                "mgmt_only": False
            }
            rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
        payload={
            "device_type": get_device_type_id(model),
            "name": "mgmt0",
            "form_factor": 1000,
            "mgmt_only": True
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))

def create_power_port_templates(model):
     url=url_base + 'api/dcim/power-port-templates/'
     for item in ['Power Supply 0','Power Supply 1']:
        payload={
            "device_type": get_device_type_id(model),
            "name": item
        }
        rest_call = requests.post(url, headers=headers, data=json.dumps(payload))

def create_prefix_roles():
    url=url_base + 'api/ipam/roles/'
    for item in my_variables_in_yaml['prefix_roles']:
     payload={
         "name": item,
         "slug": item
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'prefix role ' + item + ' successfully created'
     else:
         print 'failed to create prefix role ' + item

def get_prefix_role_id(prefix_role):
    url=url_base + 'api/ipam/roles/?name=' + prefix_role
    rest_call = requests.get(url, headers=headers)
    prefix_role_id = rest_call.json()['results'][0]['id']
    return prefix_role_id

def create_prefixes():
    url=url_base + 'api/ipam/prefixes/'
    for item in my_variables_in_yaml['prefixes']:
     payload={
           "prefix": item['prefix'],
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0]),
           "status": 1,
           "role": get_prefix_role_id(item['role'])
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'prefix ' + item['prefix'] + ' successfully created'
     else:
         print 'failed to create prefix ' + item['prefix']

def create_devices():
    url=url_base + 'api/dcim/devices/'
    custom_fields= {'dns_servers':'8.8.8.8',
                    'ntp_servers':'193.16.0.1'
                    }
    for item in my_variables_in_yaml['devices']:
     payload={
           "name": item['name'],
           "device_type": get_device_type_id(item['device_type']),
           "status": 1,
           "device_role": get_device_role_id(item['device_role']),
           "platform": get_platform_id('junos'),
           "site": get_site_id(item['site']),
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0]),
           "custom_fields":custom_fields
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'device ' + item['name'] + ' successfully created'
     else:
         print 'failed to create device ' + item['name']

def get_device_details(device):
  device_id=get_device_id(device)
  url=url_base + 'api/dcim/devices/' + str(device_id)
  rest_call = requests.get(url, headers=headers)
  pprint(rest_call.json())
  name=rest_call.json()['name']
  device_type=rest_call.json()['device_type']['id']
  status=rest_call.json()['status']['value']
  device_role=rest_call.json()['device_role']['id']
  platform=rest_call.json()['platform']['id']
  site=rest_call.json()['site']['id']
  tenant=rest_call.json()['tenant']['id']
  id=rest_call.json()['id']
  payload={
           "name": name,
           "device_type": device_type,
           "status": status,
           "device_role": device_role,
           "platform": platform,
           "site": site,
           "tenant": tenant
  }
  return payload

def create_ip_addresses(addresses):
    url=url_base + 'api/ipam/ip-addresses/'
    for item in my_variables_in_yaml[addresses]:
     device=item['device']
     interface=item['interface']
     payload={
           "status": 1,
           "address": item['ip'],
           "tenant": get_tenant_id(my_variables_in_yaml['tenants'][0]),
           "interface": get_interface_id(interface, device),
           "description": item['description']
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'address ip ' + item['ip'] + ' successfully created'
     else:
         print 'failed to create ip address ' + item['ip']

def enable_management_ip_address():
    for item in my_variables_in_yaml['adresare_management']:
     if item['mgmt_only']==True:
      device_id=get_device_id(item['device'])
      interface_id=get_interface_id(item['interface'], item['device'])
      address_id=get_address_id((item['device']), interface_id)
      url=url_base + 'api/dcim/devices/' + str(device_id) + '/'
      payload={
          "primary_ip4": address_id
      }
      rest_call = requests.patch(url, headers=headers, data=json.dumps(payload))

def get_address_id(device, interface_id):
    url=url_base + 'api/ipam/ip-addresses/?device=' + device + '&interface_id=' + str(interface_id)
    rest_call = requests.get(url, headers=headers)
    address_id = rest_call.json()['results'][0]['id']
    return address_id

def get_device_id(device):
    url=url_base + 'api/dcim/devices/?name=' + device
    rest_call = requests.get(url, headers=headers)
    device_id = rest_call.json()['results'][0]['id']
    return device_id

def get_interface_id(interface, device):
    url=url_base + 'api/dcim/interfaces/?name=' + interface + '&device=' + device
    rest_call = requests.get(url, headers=headers)
    interface_id = rest_call.json()['results'][0]['id']
    return interface_id

def create_interface_connections():
    url=url_base + 'api/dcim/interface-connections/'
    for item in my_variables_in_yaml['interface_connections']:
     device_a=item['device_a']
     device_b=item['device_b']
     interface_a=item['interface_a']
     interface_b=item['interface_b']
     interface_a_id = get_interface_id(interface_a, device_a)
     interface_b_id = get_interface_id(interface_b, device_b)
     payload={
           "connection_status": True,
           "interface_b": interface_b_id,
           "interface_a": interface_a_id
     }
     pprint(payload)
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'interface connection between ' + item['device_a'] + ' ' + item['interface_a'] + ' and ' + item['device_b'] + ' ' + item['interface_b']  + ' successfully created'
     else:
         print 'failed to create interface connection between ' + item['device_a'] + ' ' + item['interface_a'] + ' and ' + item['device_b'] + ' ' + item['interface_b']

def get_interface_connections():
    url=url_base + 'api/dcim/interface-connections/'
    rest_call = requests.get(url, headers=headers)
    pprint(rest_call.json())

def create_circuit_types():
 url=url_base + 'api/circuits/circuit-types/'
 for item in my_variables_in_yaml['circuit_types']:
     payload={
         "name": item,
         "slug": item
     }
     rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
     if rest_call.status_code == 201:
         print 'Circuit type ' + item + ' successfully created'
     else:
         print 'failed to create circuit type ' + item

#######################################################################
# Delete functions
######################################################################

def delete_ip_addresses():
 url=url_base + 'api/ipam/ip-addresses'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/ipam/ip-addresses/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_interface_connections():
    url=url_base + 'api/dcim/interface-connections/'
    rest_call = requests.get(url, headers=headers)
    for item in rest_call.json()['results']:
       id=item['id']
       url=url_base + 'api/dcim/interface-connections/' + str(id) + '/'
       rest_call = requests.delete(url, headers=headers)

def delete_devices():
 url=url_base + 'api/dcim/devices'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/devices/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_device_types():
 url=url_base + 'api/dcim/device-types'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/device-types/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_prefixes():
 url=url_base + 'api/ipam/prefixes'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/ipam/prefixes/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_sites():
 url=url_base + 'api/dcim/sites'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/sites/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_tenants():
 url=url_base + 'api/tenancy/tenants'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/tenancy/tenants/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_device_role():
 url=url_base + 'api/dcim/device-roles'
 rest_call = requests.get(url, headers=headers)
 for item in rest_call.json()['results']:
  id=item['id']
  url=url_base + 'api/dcim/device-roles/' + str(id) + '/'
  rest_call = requests.delete(url, headers=headers)

def delete_prefix_roles():
  url=url_base + 'api/ipam/roles'
  rest_call = requests.get(url, headers=headers)
  for item in rest_call.json()['results']:
   id=item['id']
   url=url_base + 'api/ipam/roles/' + str(id) + '/'
   rest_call = requests.delete(url, headers=headers)

def delete_platforms():
  url=url_base + 'api/dcim/platforms'
  rest_call = requests.get(url, headers=headers)
  for item in rest_call.json()['results']:
   id=item['id']
   url=url_base + 'api/dcim/platforms/' + str(id) + '/'
   rest_call = requests.delete(url, headers=headers)
