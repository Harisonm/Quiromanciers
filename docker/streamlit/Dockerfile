FROM python:3.7

EXPOSE 8501

WORKDIR /usr/src/app

COPY docker/streamlit/requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD streamlit run lesQuiromanciers/web/App_UI.py