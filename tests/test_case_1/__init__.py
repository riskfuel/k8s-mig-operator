"""
TEST CASE 1
-----------

Tests creating instances for the example spec defined 
in the README.md from a state with no instances.
"""

import os, yaml

# DESIRED SPEC

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/migoperator.yml") as f:
    manifest = yaml.load(f, Loader=yaml.SafeLoader)

desired_spec = {}
for device in manifest["spec"]["nodes"]["nodehostname"]["devices"]:
    desired_spec[f"gpu-{device['gpu']}"] = {
        "migEnabled": device["migEnabled"],
        "gpuInstances": device["gpuInstances"]
    }

# CURRENT STATE

gpu_instance_profiles = {'1g.5gb': '19', '2g.10gb': '14', '3g.20gb': '9', '4g.20gb': '5', '7g.40gb': '0'}
compute_instance_profiles = {'1c.7g.40gb': '0', '2c.7g.40gb': '1', '3c.7g.40gb': '2', '4c.7g.40gb': '3', '7g.40gb': '4'}

current_state = {}
for i, gpu in enumerate(desired_spec):
    current_state[gpu] = {
        "gpu_instance_profiles": gpu_instance_profiles,
        "compute_instance_profiles": compute_instance_profiles,
        "gpu_instances": [{'gpu': i, 'profile_id': '0', 'instance_id': '0', 'placement': '0:8'}],
        "comp_instances": []
    }

# EXPECTED ACTIONS

expected_actions = [
    {
        "type": "CREATE_COMP_INSTANCE",
        "gpu": i,
        "gpu_instance_id": "0",
        "profile_id": "4"
    }
    for i in range(8)
]
