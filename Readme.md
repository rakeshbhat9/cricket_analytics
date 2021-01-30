The repo currently has two folders:
1. Scraper - This will scrape ball by ball commentary for any given cric-info live commentary link and store the data in Sqlite3 database.
2. Streamlt - Then connects to the database created above to analyse the data.

Pre-requisites:
1. Docker CE / Compose installed on the server or host machine.

Usage:
1. Clone the repo
2. Update below in the /scraper/Dockerfile
    * --url : commentary page link from cricinfo - Default = None
    * --start: Hour in 24 hour format  - Default = 4
    * --finish: Hour in 24 hour format - Default = 14
3. In docker-compose.yaml
    Update volume information -v, we will need database path to be same for both services and an additional mount for scraper logs folder.
4. run docker-compose up in the directory; first time around docker will build the images from then on it should be quick turnaround.

ToDo:
1. Scraper:
    * Add innings to the extract
    * Configure table name based on match selected
2. Streamlit:
    * Build dashboard to batsmen & bowler head to head.
