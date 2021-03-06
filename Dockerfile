# base image
FROM python:3.7

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y nfs-common \
    && rm -rf /var/lib/apt/lists/*

# streamlit-specific commands
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
    [general]\n\
    email = \"\"\n\
    " > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
    [server]\n\
    enableCORS = false\n\
    " > /root/.streamlit/config.toml'

# exposing default port for streamlit
EXPOSE 8501

# copy over and install packages
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python -m spacy download en_core_web_lg

# copying everything over
COPY . .

CMD streamlit run index.py
