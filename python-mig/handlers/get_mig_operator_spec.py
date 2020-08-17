from .utils import run_shell_cmd
import yaml
import logging
log = logging.getLogger(__name__)

def get_mig_operator_spec(operator_name : str = "example-mig-operator-auto", operator_ns : str = "default") -> dict:

    raw : str = run_shell_cmd(f"kubectl -n {operator_ns} get migoperators {operator_name} -o yaml")

    try:
        migoperator = yaml.safe_load(raw)
        spec = migoperator["spec"]
        return spec
    except Exception as e:
        log.error(e)
        return {}
