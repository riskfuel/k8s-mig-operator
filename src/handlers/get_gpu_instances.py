from typing import List
from .utils import run_shell_cmd_split

def get_gpu_instances(gpu : int) -> List[dict]:
    """
    Parse the output of "nvidia-smi mig -lci"
    :return: List of dictionaries with each mig instance's metadata
    """
    raw : str = run_shell_cmd_split(f"nvidia-smi mig -i {gpu} -lgi")
    instances : List[dict] = []

    is_header = True
    for line in raw:
        if len(line) < 1:
            continue

        if line.find("=") != -1:
            is_header = False
            continue

        if not is_header:
            if line[0] != "+":
                g = line.split()[1:-1]
                instances.append({
                    "gpu": g[0],
                    "profile_id": g[3],
                    "instance_id": g[4],
                    "placement": g[5]
                })
                
    return instances