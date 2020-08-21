from .utils import run_shell_cmd
import logging
log = logging.getLogger(__name__)

def toggle_mig(gpu : int, enable : int) -> None:
    """
    :param: gpu - index of gpu
    :param: enable - if true, enable mig and vice versa
    """
    
    raw : str = run_shell_cmd(f"nvidia-smi -i {gpu} -mig {enable}")
