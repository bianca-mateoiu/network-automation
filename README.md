# network-automation project

Network Automation project, using Netbox as Source of Truth and Ansible for configuration management

To set up on https://jlabs.juniper.net/vlabs/portal/pyez-for-junos/ run setup.sh

If you'd like to initially populate Netbox with data, use:
python Netbox\ Initial\ Setup/configure_netbox.py

To generate an Ansible dynamic inventory and dynamic host var files:
python ansible_scripts/generate_dynamic_inventory+all_host_var_files.py

To generate the host var file for one device:
python ansible_scripts/ansible_update_host_var_file.py device_name


WORK in PROGRESS
