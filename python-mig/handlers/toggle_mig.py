from .utils import run_shell_cmd
import logging
log = logging.getLogger(__name__)

def toggle_mig(gpu : int, enable : bool) -> None:
    """
    :param: gpu - index of gpu
    :param: enable - if true, enable mig and vice versa
    """

    if enable:
        log.info(f"enabling mig for gpu: {gpu}")
        raw : str = run_shell_cmd(f"nvidia-smi -i {gpu} -mig 1")
    else:
        log.info(f"disabling mig for gpu: {gpu}")
        raw : str = run_shell_cmd(f"nvidia-smi -i {gpu} -mig 0")
