# NVIDIA MIG kubernetes operator

A simple python based kubernetes operator for managing nvidia MIG instances on A100 nodes. 

## Prerequisites

### node requirements

* A kubernetes 1.17+ cluster 
* Your A100 / MIG nodes should already be members of the cluster

For nodes in which you wish to enable MIG:
* MIG is supported only on NVIDIA A100 products and associated systems using A100
* CUDA 11 and NVIDIA driver 450.36.06 or later
* CUDA 11 supported Linux operating system distributions
* nvidia-docker2 with docker 19.03 or higher



## Quickstart

If you plan to allow the operator to perform resets (currently running a reboot), see the [configuring secure node access docs](./docs/configuring-secure-node-access.md) before continuing.

```bash
helm 
```



## spec

```yaml
apiVersion: operators.riskfuel.com/v1alpha1
kind: MigOperator
metadata:
  name: mig-operator
  namespace: default
spec:
  nodes:
    # hostname of node
    - hostname: dl13
      devices:
      - id: 0
        gpu_instances:
          # Options: 7g.40gb, 4g.20gb, 3g.20gb, 2g.10gb, 1g.5gb
          - gpu_instance_profile: 3g.20gb
            compute_instances:
            - 1c.3g.20gb
            - 2c.3g.20gb
          - gpu_instance_profile: 2g.10gb
            compute_instances:
            - 2c.2g.10gb
          - gpu_instance_profile: 1g.5gb
            compute_instances:
            - 1c.1g.5gb
      ...
```

## Capabilities

- [x] deleting gpu instances if they are not requested by the operator (along with their comp instances)
- [x] creating missing gpu instances
- [x] deleting compute instances
- [x] creating compute instances
- [x] toggling mig for a gpu (requires reboot currently)
- [] identify which pods need to be killed to gracefully destroy instances

## Contributing

See contributing doc [here](./docs/contributing.md).
