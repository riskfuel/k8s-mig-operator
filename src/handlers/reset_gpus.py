from .utils import run_shell_cmd
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def reset_gpus():
    """
    Causes the pod to crash!
    """

    # THIS SHOULD BE RUNNING 
    #run_shell_cmd("ansible-playbook --become --become-user=root -i ./ansible/inventory.yml ./ansible/reset-gpu-playbook.yml")

    # BUT INSTEAD WE ARE REBOOTING DUE TO ISSUES
    log.warning("REBOOTING NODE")
    run_shell_cmd("ansible-playbook --become --become-user=root -i ./ansible/inventory.yml ./ansible/restart-node.yml")
