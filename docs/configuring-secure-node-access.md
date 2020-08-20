# Configuring secure node access from your pod

## Steps 

### Create your ssh key

```bash
ssh-keygen -t rsa
```

### Copy the public key to your node

```bash
ssh-copy-id -i ~/<pub-key-file> <username>@<host>
```

### Create your k8s secret

```bash
kubectl create secret generic migoperator-secret --from-file=ssh-privatekey=/path/to/.ssh/id_rsa --from-file=ssh-publickey=/path/to/.ssh/id_rsa.pub
```