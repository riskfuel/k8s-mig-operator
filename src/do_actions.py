from action_types import action_types

from handlers import \
    delete_gpu_instance, \
    create_gpu_instance, \
    delete_compute_instance, \
    create_compute_instance, \
    toggle_mig

def do_actions(actions, comp_instances) -> None:
    """
    Takes in a list of required actions
    and performs in the correct order.
    """

    # track whether a reset is needed 
    # to complete the desired action
    reset = False

    for action in actions:

        if action["type"] not in action_types:
            raise Exception(f"ERROR: action type '{action['type']}' is not a valid action type.")

        elif action["type"] == "DELETE_GPU_INSTANCE":
            
            for i in range(action["num_instances"]):
                instance_id = action["matching_instances"].pop()

                # Comp instances must also be deleted
                for ci in comp_instances:
                    if ci["gpu_instance_id"] == instance_id:
                        delete_compute_instance(action["gpu"], instance_id, ci["instance_id"])
                delete_gpu_instance(action["gpu"], instance_id)

        elif action["type"] == "CREATE_GPU_INSTANCE":

            for i in range(action["num_instances"]):
                create_gpu_instance(action["gpu"], action["profile_id"])

        elif action["type"] == "DELETE_COMP_INSTANCE":
            for i in range(action["num_instances"]):
                gpu_instance_id = action["gpu_instance_id"]
                instance_id = action["matching_instances"].pop()
                delete_compute_instance(action["gpu"], gpu_instance_id, instance_id)

        elif action["type"] == "CREATE_COMP_INSTANCE":

            for i in range(action["num_instances"]):
                gpu_instance_id = action["gpu_instance_id"]
                create_compute_instance(action["gpu"], gpu_instance_id, action["profile_id"])
    
        elif action["type"] == "TOGGLE_MIG":
            toggle_mig(action["gpu"], action["enabled"])
            reset = True
    
    return reset
