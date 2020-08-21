from typing import List
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

from .get_gpu_instance_actions import get_gpu_instance_actions
from .get_compute_instance_actions import get_compute_instance_actions

def get_required_actions(
    gpu : int,
    desired_state : dict,
    gpu_instances : List[dict],
    comp_instances : List[dict],
    gpu_instance_profiles : dict,
    comp_instance_profiles : dict,
    mig_enabled : bool,
    reset : bool
) -> List[dict]:
    """
    Given the desired state and the current state, 
    take the required actions needed to sync the two.
    """

    actions = []

    # 1. Check if mig needs to be toggled
    
    mig_change = False
    if desired_state["migEnabled"] != mig_enabled:
        mig_change = True
        actions.append({
            "type": "TOGGLE_MIG",
            "gpu": gpu,
            "enabled": '1' if desired_state["migEnabled"] else '0'
        })

    # if we need to reset the gpus ignore all the other steps
    # they will be done upon pod restart/reset
    if mig_change or reset:
        return

    # 2. Check if gpu instances need to be created / deleted

    desired_gpu_instances = desired_state["gpuInstances"]
    gpu_instance_actions = get_gpu_instance_actions(
        gpu=gpu,
        desired_instances=desired_gpu_instances,
        gips=gpu_instance_profiles,
        current_instances=gpu_instances
    )

    # 3. Create / remove comp instances as specified or as needed 
    #                               (like in the case of deletion)

    # We already validated that our gpu instances are correct
    # so now we just need to assign our desired instances a 
    # specific instance id in order to eval comp instance state
    assigned = []
    combined_gpu_instances = [] # combine data from desired and actual into one list
    for desired_gpu_instance in desired_gpu_instances:
        for i in range(len(gpu_instances)):
            desired_profile_id = gpu_instance_profiles[desired_gpu_instance["profile"]]
            if desired_profile_id == gpu_instances[i]["profile_id"] and not i in assigned:
                assigned.append(i)
                gi = gpu_instances[i] # remove from list once attributed to a desired

                desired_gpu_instance["instance_id"] = gi["instance_id"]
                desired_gpu_instance["actualComputeInstances"] = []
                for ci in comp_instances:
                    if ci["gpu_instance_id"] == gi["instance_id"]:
                        desired_gpu_instance["actualComputeInstances"].append(ci)
                combined_gpu_instances.append(desired_gpu_instance)

    # For gpus which are to be deleted, add them to the list
    # and set their actualComputeInstances list
    for actual_gpu_instance in gpu_instances:
        in_list = False
        for gi in combined_gpu_instances:
            if actual_gpu_instance["instance_id"] == gi["instance_id"]:
                in_list = True
        if not in_list:
            actual_comp_instances = []
            for ci in comp_instances:
                if ci["gpu_instance_id"] == actual_gpu_instance["instance_id"]:
                    actual_comp_instances.append(ci)
            combined_gpu_instances.append({
                "instance_id": actual_gpu_instance["instance_id"],
                "actualComputeInstances": actual_comp_instances
            })

    comp_instance_actions = get_compute_instance_actions(
        gpu=gpu,
        gpu_instance_actions=gpu_instance_actions,
        gpu_instances=combined_gpu_instances,
        comp_instance_profiles=comp_instance_profiles
    )

    actions += comp_instance_actions
    actions += gpu_instance_actions
                
    return actions
