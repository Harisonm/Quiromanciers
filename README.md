# Run apps from python

```bash
python -m lesQuiromanciers.main
```

# Run apps from Docker


## Build container from dockerhfile
```bash
docker build . -t les_quiromanciers
```


## Run container from dockerfile
```bash
docker run \
-e LOGGER_NAME=TRANSFORM_V2 \
-e ENVIRONMENT=DEV \
-v /home/local/key:/app/key \
query_launcher \
<dataset>.<table> <args>
```


## Example
