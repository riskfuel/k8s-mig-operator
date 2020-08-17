# Contributing

## Starting the dev environment

**Note**: The dev environment assumes you are working with Ubuntu + docker installed (or a similar unix based system).

Build and enter the 
```bash
make build_shell
make shell
```

## Building the images

### Deploying the python mig daemonset

```bash
docker build -t <img>:<tag> -f ./build/Dockerfile.mig .
```

### Deploying the operator

```bash
operator-sdk build <img>:<tag>
```

## Increasing the version

*Need to decide on how this should work.*
