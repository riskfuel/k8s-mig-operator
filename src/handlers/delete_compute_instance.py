from .utils import run_shell_cmd
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def delete_compute_instance(gpu : int, gpu_instance_id : int, compute_instance_id : int) -> None:
    
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -dci -gi {gpu_instance_id} -ci {compute_instance_id}")

    log.info(f" {raw}")
