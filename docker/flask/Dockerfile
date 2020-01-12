FROM python:3.7
LABEL Author="Les Quiromanciers"
LABEL E-mail="manitra.harison@gmail.com"
LABEL version="0.0.1b"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# adduser pyuser
#!/usr/bin/env bash
ENV FN_AUTH_REDIRECT_URI=http://0.0.0.0:5000/
ENV FN_BASE_URI=http://0.0.0.0:5000
ENV OAUTHLIB_INSECURE_TRANSPORT 1
ENV FLASK_APP=lesQuiromanciers/App.py
ENV FLASK_DEBUG True
ENV FLASK_ENV=development

# development
COPY . /app
WORKDIR /app
# COPY Pip* /app/

# RUN pip install --upgrade pip && \
#     pip install pipenv && \
#     pipenv install --dev --system --deploy --ignore-pipfile

RUN pip install -r docker/flask/requirements.txt



# RUN chmod +x lesQuiromanciers/app.py && \
#     chown -R pyuser:pyuser /app

# USER pyuser
EXPOSE 5000
EXPOSE 8040

CMD flask run --host=0.0.0.0