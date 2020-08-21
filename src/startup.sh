#!/bin/bash

if [[ -z "${ALLOW_NODE_RESET}" ]]; then
python3 init_ansible.py
ansible-playbook --become --become-user=root --connection=local ./ansible/init.yml
ansible-playbook --become --become-user=root -i ./ansible/inventory.yml ./ansible/start-gpu-services.yml
fi
python3 index.py
