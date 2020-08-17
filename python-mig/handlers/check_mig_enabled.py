from .utils import run_shell_cmd_split

class MigCheckException(Exception):
    pass

def check_mig_enabled(gpu_index : int) -> bool:
    """
    Checks if MiG is enabled for a GPU
    :return: bool
    """
    cmd : str = f'nvidia-smi -i 0 --query-gpu="mig.mode.current" --format="csv"'
    raw : str = run_shell_cmd_split(cmd)
    is_enabled : bool = False

    if len(raw) < 2:
        raise MigCheckException("output does not match expected 2 line format")

    if raw[0] != "mig.mode.current":
        raise MigCheckException(f"First line should be 'mig.mode.current' not '{raw[0]}'")
    
    if raw[1] == "Enabled":
        is_enabled = True

    return is_enabled
