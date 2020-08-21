import yaml
import socket
from handlers import run_shell_cmd

def get_vars(operator_name : str = "example-mig-operator-auto", operator_ns : str = "default"):

    raw : str = run_shell_cmd(f"kubectl -n {operator_ns} get migoperators {operator_name} -o yaml")
    operator_spec : dict = yaml.safe_load(raw)
    node : str = run_shell_cmd(f"kubectl -n {operator_ns} get pod {socket.gethostname()} --output=jsonpath={{.spec.nodeName}}")
    host : str = run_shell_cmd(f"kubectl get node {node} --output=jsonpath={{.status.addresses[0].address}}")

    remote_user : str = operator_spec["spec"]["nodes"][node]["remote_user"]

    return node, host, remote_user


if __name__ == "__main__":

    hostname, hostip, remote_user = get_vars()

    # create inventory file
    inventory = {
        "all": {
            "hosts": {
                hostname: {
                    "ansible_host": hostip,
                    "ip": hostip,
                    "access_ip": hostip
                }
            }
        }
    }
    with open("./ansible/inventory.yml", "w") as f:
        yaml.dump(inventory, f)

    # create ansible vars file
    ansible_vars = {
        "remote_user": remote_user
    }
    with open("./ansible/vars.yml", "w") as f:
        yaml.dump(ansible_vars, f)
    
