from typing import List
from .utils import run_shell_cmd_split 

def get_gpus() -> dict:
    """
    returns an object in the form:
    {
        "0": "<gpu-uuid>",
        ...
    }
    """

    raw : List[str] = run_shell_cmd_split("nvidia-smi -L")
    gpus = {}

    for i, line in enumerate(raw):
        if line[0:3] == "GPU":
            g = line.split(":")
            gpus[g[0].split()[1]] = {
                "uuid": g[-1][1:-1]
            }

    return gpus
