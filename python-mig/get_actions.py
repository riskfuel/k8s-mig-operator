from typing import List
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_req_actions(
    gpu : int,
    desired_state : dict, 
    gpu_instances : List[dict],
    comp_instances : List[dict],
    gpu_instance_profiles : dict,
    mig_enabled : bool,
    reset : bool
) -> List[dict]:
    """
    Given the desired state and the current state, 
    take the required actions needed to sync the two.
    """

    actions = []
    print(desired_state)
    # if we need to reset the gpus ignore all the other steps
    # they will be done upon pod restart
    if desired_state["migEnabled"] != mig_enabled:
        toggle_mig_action = {
            "type": "TOGGLE_MIG",
            "gpu": gpu,
        }
        if desired_state["migEnabled"]:
            toggle_mig_action["enabled"] = "1"
        else:
            toggle_mig_action["enabled"] = "0"
        actions.append(toggle_mig_action)
    elif reset:
        return 
    elif not mig_enabled:
        return


    for gip in gpu_instance_profiles:
        gip_id = gpu_instance_profiles[gip]

        num_desired = 0
        num_actual = 0

        for gpu_instance in desired_state["gpuInstances"]:
            if gip_id == gpu_instance_profiles[gpu_instance["gpu_instance_profile"]]:
                num_desired += 1
        
        for gpu_instance in gpu_instances:
            if gip_id == gpu_instance["profile_id"]:
                num_actual += 1

        # log.info(f"{gip_id} ~ desired: {num_desired} ~ actual: {num_actual}")

        if num_desired != num_actual:
            if num_desired > num_actual:
                log.info(f" gpu-{gpu} - Missing {num_desired - num_actual} instances of profile_id '{gip_id}'")
                actions.append({
                    "type": "CREATE_GPU_INSTANCE",
                    "gpu": gpu,
                    "profile_id": gip_id,
                    "num_instances": num_desired - num_actual
                })
            else:
                log.info(f" gpu-{gpu} - {num_actual - num_desired} too many instances of profile_id '{gip_id}'")
                matching_instances = [ gpu_instance["instance_id"] for gpu_instance in gpu_instances if gpu_instance["profile_id"] == gip_id ]
                actions.append({
                    "type": "DELETE_GPU_INSTANCE",
                    "gpu": gpu,
                    "profile_id": gip_id,
                    "num_instances": num_actual - num_desired,
                    "matching_instances": matching_instances
                })

    return actions


