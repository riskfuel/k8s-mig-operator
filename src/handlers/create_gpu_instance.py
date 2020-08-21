from .utils import run_shell_cmd
import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

def create_gpu_instance(gpu : int, profile_id : int) -> None:
    
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -cgi {profile_id}")
    log.info(f" {raw}")
