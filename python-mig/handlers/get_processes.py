from typing import List
from .utils import run_shell_cmd_split

def get_processes(gpus : dict) -> dict:
    """
    returns an object in the form:
    {
        "0": "<gpu-uuid>",
        ...
    }
    """
    
    raw : List[str] = run_shell_cmd_split("nvidia-smi --query-compute-apps=pid,gpu_uuid,process_name,used_memory --format=csv")
    
    for i, line in enumerate(raw):
       

        if line == "" or i == 0:
            continue

        p = line.split(",")
        gpu_uuid = p[1][1:]
        gpu = {gpus[i]["uuid"]: i for i in gpus}[gpu_uuid]
        pid = p[0]
        process_name = p[2][1:]
        unused_mem = p[3][1:]

        if "processes" not in gpus[gpu]:
            gpus[gpu]["processes"] = []
        
        gpus[gpu]["processes"].append({
            "pid": pid,
            "gpu_uuid": gpu_uuid,
            "process_name": process_name,
            "unused_mem": unused_mem
        })

    return gpus
