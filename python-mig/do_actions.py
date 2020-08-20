from action_types import action_types

from handlers import \
    delete_gpu_instance, \
    create_gpu_instance, \
    toggle_mig

def do_actions(actions) -> None:
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

        if action["type"] == "DELETE_GPU_INSTANCE":
            
            for i in range(action["num_instances"]):
                instance_id = action["matching_instances"].pop()
                delete_gpu_instance(action["gpu"], instance_id)

        if action["type"] == "CREATE_GPU_INSTANCE":

            for i in range(action["num_instances"]):
                create_gpu_instance(action["gpu"], action["profile_id"])
    
        if action["type"] == "TOGGLE_MIG":
            toggle_mig(action["gpu"], action["enabled"])
            reset = True
    
    return reset
