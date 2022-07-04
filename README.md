# Car Comparison Project

## Project Description:

Recently, I've started shopping for my first car. One issue that I've noticed is the incredible amount of reviews, ratings, scores, and other metrics for every car I consider. Every site has different ratings and thoughts on each vehicle, and it becomes a task in and of itself to track all thoughts on cars you are considering. My project automates this process by scraping a range of sites to compare opinions on cars the user is interested in. *Car and Driver*, Edmunds, J.D. Power, Kelley Blue Book, *MotorTrend*, and *U.S. News & World Report* are scraped for their opinions on each car. Reliability ratings from CarEdge, Consumer Reports, and J.D. Power are also included, along with safety information from IIHS.

To accomplish this, the program prompts users for cars by their make, model, and year. The program then scrapes each site for information regarding the vehicle and properly stores the information. When the user is finished entering vehicles, CSVs are generated to help users compare reviews across sites. More detailed information from each review is stored in a site-specific CSV.

## Packages:
- [beautifulsoup4 v4.11.1](https://pypi.org/project/beautifulsoup4/) 
- [csv v1.0](https://docs.python.org/3/library/csv.html)
- [re v2.2.1](https://docs.python.org/3/library/re.html)
- [requests v2.27.1](https://pypi.org/project/requests/)

## Recent Updates:
- Extra newlines in CSV files have been removed
- Car moved to an actual class instead of being a random, informal object within `scraper.py`
- Program handles errors while reading sites much better now

## Things to improve:
- I ran into significant issues trying to scrape the pros and cons from *MotorTrend* reviews. I couldn't find a solution initially, but it's worth taking a deeper dive so that information can be extracted in the future.
- It would be better if the users had a way to interact with the program other than the terminal. A simple UI would do a great deal in helping the program to be easier for some to use
- The program's speed would (hopefully) increase if all scraping was done in parallel rather than one at a time between user entries. I'm not entirely sure if parallel operations like this are possible with Python, but it is definitely worth investigating.