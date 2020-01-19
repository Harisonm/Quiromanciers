# Run apps from python

## Run project from root path
```bash
streamlit run LesQuiromanciersUI.py
```

# Run apps from Docker

## Build container from dockerhfile
```bash
docker build . -t les-quiromanciers
```


## Run container from dockerfile
```bash
docker run -d -p 8501:8501 les-quiromanciers
```

### create tag container
```
docker tag les-quiromanciers gcr.io/neomail-258716/les-quiromanciers:latest
```

### Push tag container
```
docker push gcr.io/neomail-258716/les-quiromanciers:latest
```


# Configure Workflows to GKE

This workflow will build a docker container, publish it to Google Container Registry, and deploy it to GKE.

To configure this workflow:

1. Ensure that your repository contains the necessary configuration for your Google Kubernetes Engine cluster, including deployment.yml, kustomization.yml, service.yml, etc.

2. Set up secrets in your workspace: GKE_PROJECT with the name of the project, GKE_EMAIL with the service account email, GKE_KEY with the service account key.

3. Change the values for the GKE_ZONE, GKE_CLUSTER and IMAGE environment variables (below).