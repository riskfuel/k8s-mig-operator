# k8s mig operator design

## Motivation

As of writing this (Aug 17 2020), there is to our knowledge, no easy way dynamically provision/manage MIG gpu instances using kubernetes. Additionally, the process for getting a k8s cluster containing A100 nodes ready for MIG instance allocation is also a bit unclear. Thus this operator serves two main purposes:
1. Bring together all the required manifests needed to allocate MIG instances to pods
2. Provide a kube-apiserver interface for specifying the desired state of MIG instances across A100 nodes 

## k8s MIG operator

The operator is responsible for managing the following resources along with their required rbac components:
* The node feature discovery daemonset
* The gpu feature discovery daemonset
* The nvidia k8s device plugin daemonset
* The mig-operator daemonset

## MIG instance management

At a high level the process flows as follows:
* Retrieve the desired state of the node from the kube-apiserver via the migoperators.operators.riskfuel.com CRD
* Evaluate the current state of the node by running and parsing `nvidia-smi` commands from inside a privilidged pod
* Run the `nvidia-smi` commands required to sync up the desired state with the actual node state

This is all being done using python and its `subprocess` module to pipe the output of the commands into parsable strings.

### Required nvidia-smi commands

#### Check if MIG is enabled by a device

```bash
nvidia-smi -i 0 --query-gpu="mig.mode.current" --format="csv"
```

#### List the current compute instances

```bash
nvidia-smi mig -lci
```
#### Set the MIG strategy

#### Toggle MIG
*Note: GPU reset is required after enabling / disabling MIG as well as when changing the MIG strategy*

```bash
nvidia-smi -i 0 -mig 1 # Enables MIG on GPU 0
nvidia-smi -i 0 -mig 0 # Disables MIG on GPU 0
```

#### MIG instance creation

```bash
nvidia-smi mig -cgi 9,9 # Create 2 GPU instances with profile 9
```

#### Compute instance creation
```bash
nvidia-smi mig -cci -gi 1,2   # Create 2 compute instances (default profile) using GPU instance 1 and 2
```

#### MIG instance teardown

```bash
nvidia-smi mig -dci -ci 1,2 -gi 1 # Destroys compute instances 1 and 2 on GPU instance 1
```