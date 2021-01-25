FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY streamlit.py streamlit.py
CMD ["streamlit","run","streamlit.py"]