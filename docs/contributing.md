# Contributing

If this project interests you, feel free to contact us directly via email:
- addyvan (addison): addison@riskfuel.com

## Starting the dev environment

Seeing as access to A100 features isn't widespread, there is no dev environment. Everything is currently being testing on a k8s cluster.

## Rollouts

### Deploying the mig-operator daemonset

* Handled by one of the jobs in `.github/`

### Increasing the version

Increasing the version triggers a github release containing the new helm chart, updates the helm index, and builds a new container. It also triggers all future docker container builds to use the new tag. 
