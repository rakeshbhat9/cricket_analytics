FROM python:3.8-slim-buster
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt
COPY comm_scraper.py comm_scraper.py
CMD ["python","comm_scraper.py",\
    "--url","https://www.espncricinfo.com/series/england-in-sri-lanka-2020-21-1242951/sri-lanka-vs-england-2nd-test-1243016/live-cricket-score",\
    "--start","21","--finish","23"]