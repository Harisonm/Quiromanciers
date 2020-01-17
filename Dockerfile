FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8501

CMD streamlit run LesQuiromanciersUI.py