from .utils import run_shell_cmd
import logging
log = logging.getLogger(__name__)

def create_gpu_instance(gpu : int, profile_id : int) -> None:
    
    log.info(f"Creating gpu instance on gpu '{gpu}' using profile id '{profile_id}'")
    raw : str = run_shell_cmd(f"nvidia-smi mig -i {gpu} -cgi {profile_id}")
    log.info(raw)
