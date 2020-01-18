# Run apps from python

## Run project from root path
```bash
streamlit run LesQuiromanciersUI.py
```

# Run apps from Docker

## Build container from dockerhfile
```bash
docker build . -t les_quiromanciers
```


## Run container from dockerfile
```bash
docker run -d -p 8501:8501 les_quiromanciers
```