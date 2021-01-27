FROM debian:buster-slim
RUN  apt update && apt upgrade -y
RUN  apt install python3-pip -y && apt install python3-pandas -y
COPY requirements.txt .
RUN  pip3 install --user -r requirements.txt
COPY comm_scraper.py comm_scraper.py
CMD ["python3","comm_scraper.py",\
    "--url","https://www.espncricinfo.com/series/south-africa-in-pakistan-2020-21-1242968/pakistan-vs-south-africa-1st-test-1243017/live-cricket-score"]