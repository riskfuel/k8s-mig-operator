from typing import List
from datetime import datetime
from .utils import load_context
load_context()

from .action_types import action_types

from handlers import \
    delete_gpu_instance, \
    create_gpu_instance, \
    delete_compute_instance, \
    create_compute_instance, \
    toggle_mig

import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)


def perform_actions(actions : List[dict]) -> None:
    """
    Takes in a list of required actions
    and performs in the correct order.
    """

    # track whether a reset is needed 
    # to complete the desired action
    reset = False

    for action in actions:

        now = datetime.now()
        t = now.strftime("%m/%d/%Y, %H:%M:%S")
        log.info(f" {t} - gpu{action['gpu']}: <{action['type']}> ")

        if action["type"] not in action_types:
            raise Exception(f"ERROR: action type '{action['type']}' is not a valid action type.")

        elif action["type"] == "DELETE_GPU_INSTANCE":
            instance_id = action["instance_id"]
            delete_gpu_instance(action["gpu"], instance_id)

        elif action["type"] == "CREATE_GPU_INSTANCE":
            create_gpu_instance(action["gpu"], action["profile_id"])

        elif action["type"] == "DELETE_COMP_INSTANCE":
            gpu_instance_id = action["gpu_instance_id"]
            instance_id = action["instance_id"]
            delete_compute_instance(action["gpu"], gpu_instance_id, instance_id)

        elif action["type"] == "CREATE_COMP_INSTANCE":
            gpu_instance_id = action["gpu_instance_id"]
            create_compute_instance(action["gpu"], gpu_instance_id, action["profile_id"])
    
        elif action["type"] == "TOGGLE_MIG":
            toggle_mig(action["gpu"], action["enabled"])
            reset = True
    
    return reset
