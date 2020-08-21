from typing import List
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_compute_instance_actions(
    gpu : int,
    gpu_instance_actions : List[dict],
    gpu_instances : List[dict],
    comp_instance_profiles : dict, 
) -> List[dict]:
    """
    Compute required nvidia-smi actions needed to sync up desired 
    and current state.

    """

    

    actions = []

    # if gpu instances need updating, we will
    # perform comp instance actions in the next cycle
    # the only exception here is that we need to make sure
    # that gpu instances that are set to be deleted have
    # their comp instances removed first (or flagged)
    if len(gpu_instance_actions) > 0:
        for gpu_action in gpu_instance_actions:
            if gpu_action["type"] == "DELETE_GPU_INSTANCE":
                gpu_instance = {gi["instance_id"]:gi for gi in gpu_instances}[gpu_action["instance_id"]]
                if len(gpu_instance["actualComputeInstances"]) > 0:
                    for ci in gpu_instance["actualComputeInstances"]:
                        actions.append({
                            "type": "DELETE_COMP_INSTANCE",
                            "gpu": gpu,
                            "gpu_instance_id": gpu_instance["instance_id"],
                            "instance_id": ci["instance_id"]
                        })    
    # Only create/delete comp instances
    # if the state of gpu instances is 
    # correct / stable
    else:
        for gpu_instance in gpu_instances:
            for cip in comp_instance_profiles:
                cip_id = comp_instance_profiles[cip]
                num_desired = 0
                num_actual = 0

                for d in gpu_instance["computeInstances"]:
                    if cip_id == comp_instance_profiles[d]:
                        num_desired += 1
                
                for comp_instance in gpu_instance["actualComputeInstances"]:
                    if cip_id == comp_instance["profile_id"]:
                        num_actual += 1

                if num_desired != num_actual:
                    if num_desired > num_actual:
                        
                        for i in range(num_desired - num_actual):
                            actions.append({
                                "type": "CREATE_COMP_INSTANCE",
                                "gpu": gpu,
                                "gpu_instance_id": gpu_instance["instance_id"],
                                "profile_id": cip_id
                            })

                    else:
                        matching_instances = [ci["instance_id"] for ci in gpu_instance["actualComputeInstances"] if ci["profile_id"] == cip_id]
                        for i in range(num_actual - num_desired):
                            actions.append({
                                "type": "DELETE_COMP_INSTANCE",
                                "gpu": gpu,
                                "gpu_instance_id": gi["instance_id"],
                                "instance_id": matching_instances.pop()
                            })

    return actions
