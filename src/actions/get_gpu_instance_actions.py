from typing import List
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def get_gpu_instance_actions(
    gpu : int,
    desired_instances : List[dict],
    gips : dict,
    current_instances : List[dict]
) -> List[dict]:
    """
    Compute required nvidia-smi actions needed to sync up desired 
    and current state.
    :param: gpu - index of gpu
    :param: desired_instances - List of desired gpu instances
    :param: gips - gpu instance profiles dict
    :param: current_instances - List of current gpu instances
    """
    actions = []
    for gip in gips:
        gip_id = gips[gip]

        num_desired = 0
        num_actual = 0

        for gpu_instance in desired_instances:
            if gip_id == gips[gpu_instance["profile"]]:
                num_desired += 1
        
        for gpu_instance in current_instances:
            if gip_id == gpu_instance["profile_id"]:
                num_actual += 1

        if num_desired != num_actual:
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
                matching_instances = [ gpu_instance["instance_id"] for gpu_instance in current_instances if gpu_instance["profile_id"] == gip_id ]
                for i in range(num_actual - num_desired):
                    actions.append({
                        "type": "DELETE_GPU_INSTANCE",
                        "gpu": gpu,
                        "instance_id": matching_instances.pop()
                    })
    return actions