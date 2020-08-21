from .utils import run_shell_cmd
import yaml
import logging
import socket

log = logging.getLogger(__name__)

def get_operator_spec(operator_name : str, operator_ns : str) -> dict:

    raw : str = run_shell_cmd(f"kubectl -n {operator_ns} get migoperators {operator_name} -o yaml")
    node : str = run_shell_cmd(f"kubectl -n {operator_ns} get pod {socket.gethostname()} --output=jsonpath={{.spec.nodeName}}")

    spec = {}
    try:
        migoperator = yaml.safe_load(raw)

        for device in migoperator["spec"]["nodes"][node]["devices"]:
            spec[f"gpu-{device['gpu']}"] = {
                "migEnabled": device["migEnabled"],
                "gpuInstances": device["gpuInstances"]
            }
            
        return spec
    except Exception as e:
        log.error(e)
        return {}
