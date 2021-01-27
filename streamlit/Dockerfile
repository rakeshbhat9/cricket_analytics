FROM debian:buster-slim
RUN  apt update && apt upgrade -y
RUN  apt install python3-pip -y && apt install python3-pandas -y
COPY requirements.txt requirements.txt
RUN  pip3 install -r requirements.txt
EXPOSE 8501
COPY streamlit.py streamlit.py
CMD ["streamlit","run","streamlit.py"]