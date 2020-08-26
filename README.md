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

### Install the operator daemons

```bash
helm repo add k8s-mig-operator https://riskfuel.github.io/k8s-mig-operator/
helm repo update
helm install mig-operator k8s-mig-operator/k8s-mig-operator \
  --version=0.1.1 \
  --set deployNamespace=default \
  --set dryRun=false \
  --set allowNodeReset=true \
  --set sshSecretName=migoperator-secret \
  --set deployNvidiaPlugins=true \
  --set operatorName=example-mig-operator \
  --set operatorNamespace=default \
  --set image=riskfuel/k8s-mig-operator:0.1.1
```

### Create an operator CRD

*Note:* You can use the examples in `deployments/examples` as a base.

```
kubectl apply -f <example-mig-operator>
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
    nodehostname:

      remote_user: remote-user

      # if not specified, features like toggling mig
      # or switching strategies wont be available
      secretName: migoperator-secret

      # Options for MIG instance profiles: 7g.40gb, 4g.20gb, 3g.20gb, 2g.10gb, 1g.5gb
      # Options for compute instance profiles: 7g.40gb, 4c.xg.ygb, 3c.xg.ygb, 2c.xg.ygb, 1c.xg.ygb
      # NOTE: nvidia-device-plugin does not support non default compute sizes, however
      #       we still currently support creating these instances. 
      devices:
      - gpu: 0
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 1
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 2
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 3
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 4
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 5
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 6
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
      - gpu: 7
        migEnabled: True
        gpuInstances:
        - profile: 7g.40gb
          computeInstances:
          - 7g.40gb
```

## Capabilities

- [x] delete gpu instances if they are not requested by the operator 
  - also removes any comp instances on the gpu instance
- [x] create missing gpu instances
- [x] delete compute instances
- [x] create compute instances
- [x] toggle mig for a gpu (requires reboot/reset currently)

## Contributing

See contributing doc [here](./docs/contributing.md).
