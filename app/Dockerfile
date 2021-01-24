FROM python:3.8-slim-buster
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
COPY comm_scraper.py .
ENTRYPOINT [ "python","comm_scraper.py"]