FROM python:3.7

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN pip install https://storage.googleapis.com/intel-optimized-tensorflow/intel_tensorflow-1.14.0-cp37-cp37m-manylinux1_86_64.whl

COPY . /app
WORKDIR /app

# ENTRYPOINT [ "python", "-m", "lesQuiromanciers.main"]
