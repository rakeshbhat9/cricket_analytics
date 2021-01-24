Script scrapes ball by ball commentary from CricInfo for any given match.

Pre-requisites:
1. Docker installed on the machine.

Steps:
1. Create a sqlite3 db on your local host machine with name cricinfo_raw.db and create a table called raw.

2. Then simply run the below docker run command where;

    a. -v : Abs path of the sqlite3 db on local host.

    Flags below are python script specific managed by click and not docker run command flags.

    b. --url : commentary page link from cricinfo

    The container will run perpetually hence by passing below hour flags we can get control when the script actually sources the data.

    c. --start: Hour in 24 hour format
    d. --finish: Hour in 24 hour format

        docker run --rm -it \
                -v /home/rakeshbhat9/repos/databases/cricinfo_raw.db:/cricinfo_raw.db rakeshbhat9/cricket_commentary_scraper:latest \
                --url 'https://www.espncricinfo.com/series/england-in-sri-lanka-2020-21-1242951/sri-lanka-vs-england-2nd-test-1243016/live-cricket-score' \
                --start 20 \
                --finish 22
    
    e. You can run the container as below to get help on arguments.
    
        docker run --rm -it rakeshbhat9/cricket_commentary_scraper:latest --help
