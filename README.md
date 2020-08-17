# NVIDIA MIG kubernetes operator

A kubernetes operator designed to manage nvidia MIG instances on the DGX A100 without leaving kubernetes. 

## Prerequisites

* A kubernetes 1.17+ cluster 
* Your A100 / MIG nodes should already be members of the cluster

For nodes in which you wish to enable MIG:
* MIG is supported only on NVIDIA A100 products and associated systems using A100
* CUDA 11 and NVIDIA driver 450.36.06 or later
* CUDA 11 supported Linux operating system distributions
* nvidia-docker2 with docker 19.03 or higher

## Quickstart

```bash
kubectl apply -f <release-yml>
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
    dl13:
      gpu_instances:
      - 
      compute_instances:
      - 
```

## Checking if a node is compatible

You can check to see a specific node's compatibility by running the following:

**NOTE:** Make sure to first edit the node affinity on line 21 of `./deployments/node-mig-discovery.yml` in order to select the node which you would like to run `nvidia-smi` on. 

```bash
kubectl apply -f ./deployments/node-mig-discovery.yml
kubectl wait --for=condition=ready pod node-mig-discovery
kubectl exec -it node-mig-discovery -- nvidia-smi
kubectl exec -it node-mig-discovery -- nvidia-smi
kubectl delete -f ./deployments/node-mig-discovery.yml
```

This will output information about the GPUs associated with your machine. You should see: 
* The following version info: `NVIDIA-SMI 450.51.06    Driver Version: 450.51.06    CUDA Version: 11.0`
* On the right hand side of the first table there should be a `MIG M.` variable which is set to disabled by default. 

## Contributing

See contributing doc [here](./docs/contributing.md).
