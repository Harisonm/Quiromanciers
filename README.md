# Run apps from python

## Run project from root path
```bash
python -m lesQuiromanciers.main
```

## Run Flask from bash
```bash
bash sh/run_flask.sh
```

# Run apps from Docker

## Build container from dockerhfile
```bash
docker build . -t les_quiromanciers
```


## Run container from dockerfile
```bash
docker run -d -p 8040:8040 les_quiromanciers
```
