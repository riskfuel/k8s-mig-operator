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
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

from handlers import \
    run_shell_cmd, \
    get_operator_spec, \
    get_gpu_instances, \
    get_compute_instances, \
    check_mig_enabled, \
    get_gpu_instance_profiles, \
    get_compute_instance_profiles, \
    get_gpus, \
    get_processes, \
    reset_gpus

from get_actions import get_req_actions
from do_actions import do_actions

def sync_loop() -> None:
    """
    * retrieves desired state
    * evaluates the current state
    * runs nvidia-smi commands to sync the two
    """
    log.info("Running sync loop...")

    desired_spec = get_operator_spec()
    gpus : dict = get_gpus()
    gpus : dict = get_processes(gpus)
    
    reset = False
    for gpu_index in gpus:
        i = int(gpu_index)
        
        if f"gpu-{i}" not in desired_spec:
            continue

        gpu_instance_profiles : dict = get_gpu_instance_profiles(i)
        compute_instance_profiles : dict = get_compute_instance_profiles(i)
        mig_gpu_instances : List[dict] = get_gpu_instances(i)
        mig_comp_instances : List[dict] = get_compute_instances(i)

        actions = get_req_actions(
            i, 
            desired_spec[f"gpu-{i}"], 
            mig_gpu_instances,
            mig_comp_instances,
            gpu_instance_profiles,
            compute_instance_profiles,
            check_mig_enabled(i),
            reset
        )

        if do_actions(actions, mig_comp_instances):
            reset = True

    if reset:
        reset_gpus()


if __name__ == "__main__":

    while True:
        sync_loop()
        time.sleep(5)
