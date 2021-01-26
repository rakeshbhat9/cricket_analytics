FROM python:3.8-slim-buster
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
COPY comm_scraper.py comm_scraper.py
CMD ["python","comm_scraper.py",\
    "--url","https://www.espncricinfo.com/series/south-africa-in-pakistan-2020-21-1242968/pakistan-vs-south-africa-1st-test-1243017/live-cricket-score"]