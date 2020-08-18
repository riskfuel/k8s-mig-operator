"""
MIG Sidecar

Note: As of writting this code, pynvml does not support mig commands
      As such, the code below parses the outputs of running commands
      using the nvidia-smi CLI.

The mig sidecar runs in a loop and is responsible for:
-> parsing the desired state received from the MigOperator
-> evaluating the current state of the node in which 

authors: 
- addison@riskfuel
"""

import time
import os
from typing import List

import logging
log = logging.getLogger(__name__)

from handlers import \
    get_mig_operator_spec, \
    get_mig_gpu_instances, \
    get_mig_compute_instances, \
    check_mig_enabled, \
    get_gpu_instance_profiles

def select_actions(desired_spec : dict) -> List[dict]:
    pass

def sync_loop() -> None:
    """
    * retrieves desired state
    * evaluates the current state
    * runs nvidia-smi commands to sync the two
    """
    print("Starting sync loop...")

    desired_spec = get_mig_operator_spec()
    print("\n\n\n")
    print("---- DESIRED SPEC ----")
    print(desired_spec)
    print("\n\n")

    print("---- GPU_INSTANCE_PROFILES ----")

    gpu_instance_profiles = get_gpu_instance_profiles()
    print(gpu_instance_profiles)

    print("\n\n")

    print("---- CURRENT MIG GPU INSTANCES ----")

    gpu_instances = get_mig_gpu_instances()
    print(gpu_instances)

    print("\n\n")
    print("---- CURRENT MIG COMPUTE INSTANCES ----")
    mig_comp_instances : List[dict] = get_mig_compute_instances()
    print(f"current mig instances: {mig_comp_instances}")
    print("\n\n")

    print("---- MIG AVAILABILITY BY GPU ----")
    try:
        for i in range(8):
            print(f"GPU-{i} mig enabled: {check_mig_enabled(i)}")
    except Exception as e:
        log.error(e)
        


if __name__ == "__main__":
    
    while True:
        sync_loop()
        time.sleep(10)
