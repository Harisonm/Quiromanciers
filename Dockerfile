FROM python:3.7
LABEL Author="Les Quiromanciers"
LABEL E-mail="manitra.harison@gmail.com"
LABEL version="0.0.1b"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# adduser pyuser
#!/usr/bin/env bash
ENV FN_AUTH_REDIRECT_URI "http://127.0.0.1:8040/"
ENV FN_BASE_URI "http://127.0.0.1:8040"
ENV OAUTHLIB_INSECURE_TRANSPORT 1
ENV FLASK_APP "lesQuiromanciers/backend/app.py"
ENV FLASK_DEBUG True
ENV FLASK_ENV "development"

# development
COPY . /app
WORKDIR /app
# COPY Pip* /app/

# RUN pip install --upgrade pip && \
#     pip install pipenv && \
#     pipenv install --dev --system --deploy --ignore-pipfile

RUN pip install -r requirements.txt



# RUN chmod +x lesQuiromanciers/app.py && \
#     chown -R pyuser:pyuser /app

# USER pyuser
EXPOSE 5000
EXPOSE 8040

CMD flask run -p 8040 --host=127.0.0.1