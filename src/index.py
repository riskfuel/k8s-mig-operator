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
from datetime import datetime
import os
from typing import List

import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

from settings import settings

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

from actions import \
    get_required_actions, \
    perform_actions

dry_run = settings["DRY_RUN"]

def sync_loop() -> None:
    """
    * retrieves desired state
    * evaluates the current state
    * runs nvidia-smi commands to sync the two
    """
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    log.info(f" {t} Running sync loop...")

    desired_spec = get_operator_spec(settings["OPERATOR_NAME"], settings["OPERATOR_NAMESPACE"])
    gpus : dict = get_gpus()
    gpus : dict = get_processes(gpus)
    
    actions = []
    reset = False
    for gpu_index in gpus:
        i = int(gpu_index)
        
        if f"gpu-{i}" not in desired_spec:
            continue

        gpu_instance_profiles : dict = get_gpu_instance_profiles(i)
        compute_instance_profiles : dict = get_compute_instance_profiles(i)
        gpu_instances : List[dict] = get_gpu_instances(i)
        comp_instances : List[dict] = get_compute_instances(i)

        actions += get_required_actions(
            i, 
            desired_spec[f"gpu-{i}"], 
            gpu_instances,
            comp_instances,
            gpu_instance_profiles,
            compute_instance_profiles,
            check_mig_enabled(i),
            reset
        )
        for action in actions:
            if action["type"] == "TOGGLE_MIG":
                reset = True
    
    log.info("\n ACTIONS \n")
    for action in actions:
        log.info(f" {action} ")

    if not dry_run:
        perform_actions(actions)

        if reset:
            reset_gpus()


if __name__ == "__main__":

    if settings["ALLOW_NODE_RESET"]:
        run_shell_cmd("python3 init_ansible.py")
        run_shell_cmd("ansible-playbook --become --become-user=root --connection=local ./ansible/init.yml")
        run_shell_cmd("ansible-playbook --become --become-user=root -i ./ansible/inventory.yml ./ansible/start-gpu-services.yml")

    while True:
        sync_loop()
        time.sleep(5)
