# base image
FROM python:3.7

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

# copy over and install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt


# exposing default port for streamlit
EXPOSE 8501

# copying everything over
COPY . .

CMD streamlit run LesQuiromanciersUI.py