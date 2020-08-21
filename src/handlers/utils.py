from typing import List
from subprocess import Popen, PIPE
import os

def run_shell_cmd_split(command : str) -> List[str]:
    """
    :param: command - string containing desired nvidia-smi command
                        e.g nvidia-smi mig -lcip
    :return: a list of strings containing each line returned by the command
    """
    try:
        p = Popen(command, stdout=PIPE, shell=True)
        stdout, stderr = p.communicate()
    except Exception as e:
        return f"ERROR {e}"

    output = stdout.decode('UTF-8')
    lines = output.split(os.linesep)
    return lines

def run_shell_cmd(command : str) -> str:
    """
    :param: command - string containing desired nvidia-smi command
                        e.g nvidia-smi mig -lcip
    :return: a list of strings containing each line returned by the command
    """
    try:
        p = Popen(command, stdout=PIPE, shell=True)
        stdout, stderr = p.communicate()
    except Exception as e:
        return f"ERROR {e}"

    output = stdout.decode('UTF-8')
    return output
