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
    comp_instance_profiles : dict,
    mig_enabled : bool,
    reset : bool
) -> List[dict]:
    """
    Given the desired state and the current state, 
    take the required actions needed to sync the two.
    """

    actions = []
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
        print("reset toggled")
        return 

    gpu_instances_need_update = False
    for gip in gpu_instance_profiles:
        gip_id = gpu_instance_profiles[gip]


        # GPU INSTANCES

        num_desired = 0
        num_actual = 0

        for gpu_instance in desired_state["gpuInstances"]:
            if gip_id == gpu_instance_profiles[gpu_instance["gpu_instance_profile"]]:
                num_desired += 1
        
        for gpu_instance in gpu_instances:
            if gip_id == gpu_instance["profile_id"]:
                num_actual += 1

        if num_desired != num_actual:
            gpu_instances_need_update = True
            if num_desired > num_actual:
                log.info(f" gpu-{gpu} - Missing {num_desired - num_actual} gpu instances of profile_id '{gip_id}'")
                actions.append({
                    "type": "CREATE_GPU_INSTANCE",
                    "gpu": gpu,
                    "profile_id": gip_id,
                    "num_instances": num_desired - num_actual
                })
            else:
                log.info(f" gpu-{gpu} - {num_actual - num_desired} too many gpu instances of profile_id '{gip_id}'")
                matching_instances = [ gpu_instance["instance_id"] for gpu_instance in gpu_instances if gpu_instance["profile_id"] == gip_id ]
                
                actions.append({
                    "type": "DELETE_GPU_INSTANCE",
                    "gpu": gpu,
                    "profile_id": gip_id,
                    "num_instances": num_actual - num_desired,
                    "matching_instances": matching_instances
                })



    # COMP INSTANCES

    # if gpu instances need updating, we will
    # eval comp instances in the next cycle
    if not gpu_instances_need_update:

        
        d = [] # new list containing instance_id to be made
        for desired_gpu_instance in desired_state["gpuInstances"]:
            for i in range(len(gpu_instances)):
                if gpu_instance_profiles[desired_gpu_instance["gpu_instance_profile"]] == gpu_instances[i]["profile_id"]:
                    gi = gpu_instances.pop(i)
                    
                    desired_comp = desired_gpu_instance["compute_instances"]

                    actual_comp = []
                    for ci in comp_instances:
                        if ci["gpu_instance_id"] == gi["instance_id"]:
                            actual_comp.append(ci)

                    for cip in comp_instance_profiles:
                        cip_id = comp_instance_profiles[cip]
                        num_desired = 0
                        num_actual = 0

                        for d in desired_comp:
                            if cip_id == comp_instance_profiles[d]:
                                num_desired += 1
                        
                        for comp_instance in actual_comp:
                            if cip_id == comp_instance["profile_id"]:
                                num_actual += 1

                        if num_desired != num_actual:
                            if num_desired > num_actual:
                                log.info(f" gpu-{gpu} - gpu instance {gi['instance_id']} - Missing {num_desired - num_actual} comp instances of profile_id '{cip_id}'")
                                actions.append({
                                    "type": "CREATE_COMP_INSTANCE",
                                    "gpu": gpu,
                                    "gpu_instance_id": gi["instance_id"],
                                    "num_instances": num_desired - num_actual,
                                    "profile_id": cip_id
                                })
                            else:
                                log.info(f" gpu-{gpu} - gpu instance {gi['instance_id']} - {num_actual - num_desired} too many comp instances of profile_id '{cip_id}'")
                                matching_instances = []
                                for ci in actual_comp:
                                    if ci["profile_id"] == cip_id:
                                        matching_instances.append(ci["instance_id"])
                                actions.append({
                                    "type": "DELETE_COMP_INSTANCE",
                                    "gpu": gpu,
                                    "gpu_instance_id": gi["instance_id"],
                                    "num_instances": num_actual - num_desired,
                                    "matching_instances": matching_instances
                                })
                        elif num_desired > 0:
                            log.info(f"  {cip} correctly scheduled at {num_desired} instances for gpu instance {gi['instance_id']} on gpu {gpu}")
                        else:
                            log.info(f"  {cip} desired: {num_desired} instances vs actual {num_actual} for gpu instance {gi['instance_id']} on gpu {gpu}")
                

    return actions


