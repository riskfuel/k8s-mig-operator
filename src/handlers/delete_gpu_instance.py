from .utils import run_shell_cmd
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def delete_gpu_instance(gpu : int, instance_id : int) -> None:
    
    log.info(f" Destroying gpu instance '{instance_id}' on gpu '{gpu}'. ")
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -dgi -gi {instance_id}")

    log.info(f" SHELL OUTPUT: {raw}")
