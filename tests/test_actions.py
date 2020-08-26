import pytest
from load_context import load_context
load_context()

from actions import get_required_actions
from test_case_1 import \
    desired_spec, \
    current_state, \
    expected_actions

testdata = [
    (current_state, desired_spec, expected_actions),
]

def get_actions(current_state, desired_spec, expected_actions):
    actions = []
    for i in range(8):
        gpu_instance_profiles = current_state[f"gpu-{i}"]["gpu_instance_profiles"]
        compute_instance_profiles = current_state[f"gpu-{i}"]["compute_instance_profiles"]
        gpu_instances = current_state[f"gpu-{i}"]["gpu_instances"]
        comp_instances = current_state[f"gpu-{i}"]["comp_instances"]

        actions += get_required_actions(
            i, 
            desired_spec[f"gpu-{i}"], 
            gpu_instances,
            comp_instances,
            gpu_instance_profiles,
            compute_instance_profiles,
            True,
            False
        )

    return actions

@pytest.mark.parametrize("current_state,desired_spec,expected_actions", testdata)
def test_action_selection(current_state, desired_spec, expected_actions):
    """
    Ensure correct actions are being triggered
    :param: current_state
    :param: desired_spec
    :param: expected_actions
    """
    
    actions = get_actions(*testdata[0])
    for i, desired_action in enumerate(expected_actions):
        assert desired_action == actions[i]
