from .utils import run_shell_cmd_split

def get_gpu_instance_profiles(gpu : int) -> dict:

    raw : str = run_shell_cmd_split(f"nvidia-smi mig -i {gpu} -lgip")
    gpu_instance_profiles : dict = {}

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
                if g[1] == "MIG":
                    gpu_instance_profiles[g[2]] = g[3]

    return gpu_instance_profiles
