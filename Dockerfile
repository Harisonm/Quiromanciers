FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt && \
    #!/usr/bin/env bash
    export FN_AUTH_REDIRECT_URI=http://127.0.0.1:8040/ && \
    export FN_BASE_URI=http://127.0.0.1:8040 && \
    export OAUTHLIB_INSECURE_TRANSPORT=1 && \
    export FLASK_APP=lesQuiromanciers/app.py && \
    export FLASK_DEBUG=1 && \
    export FLASK_ENV=development && \
    adduser pyuser && \
    export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET

# development
COPY . /app
WORKDIR /app

RUN chmod +x lesQuiromanciers/app.py && \
    chown -R pyuser:pyuser /app

USER pyuser
EXPOSE 5000
EXPOSE 8040

CMD flask run -p 8040 --host=127.0.0.1