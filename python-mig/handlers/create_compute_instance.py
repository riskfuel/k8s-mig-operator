from .utils import run_shell_cmd
import logging
log = logging.getLogger(__name__)

def create_compute_instance(gpu : int, instance_id : int) -> None:
    """
    :param: gpu - index of gpu
    :param: instance_id - instance id of the parent gpu instance
    """
    
    log.info(f"Creating compute instance using instance id '{instance_id}' on gpu '{gpu}'")
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -cci -gi {instance_id}")
    log.info(raw)
