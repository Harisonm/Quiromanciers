#!/usr/bin/env bash
export FN_AUTH_REDIRECT_URI=http://127.0.0.1:8040/
export FN_BASE_URI=http://127.0.0.1:8040
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=lesQuiromanciers/app.py
export FLASK_DEBUG=1
export FLASK_ENV=development
# development
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET

python -m flask run -p 8040 --host=127.0.0.1
