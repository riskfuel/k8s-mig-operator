from .utils import run_shell_cmd
import yaml

def get_mig_operator_spec(operator_name : str = "example-mig-operator-auto", operator_ns : str = "default") -> dict:

    raw : str = run_shell_cmd(f"kubectl -n {operator_ns} get migoperators {operator_name} -o yaml")

    migoperator = yaml.safe_load(raw)
    spec = migoperator["spec"]
    return spec
