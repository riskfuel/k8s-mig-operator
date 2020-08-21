from .utils import run_shell_cmd
import logging
log = logging.getLogger(__name__)

def create_compute_instance(gpu : int, gpu_instance_id : int, profile_id : int) -> None:
    """
    :param: gpu - index of gpu
    :param: gpu_instance_id - instance id of the parent gpu instance
    """
    
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -gi {gpu_instance_id} -cci {profile_id}")
    log.info(f" {raw}")
