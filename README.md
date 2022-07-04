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

## Things to improve:
- It would be much better if the cars that were created in `scraper.py` were formal objects. This would help the program to better follow Object-Oriented principles
- More graceful exits when the program runs into scraping issues is a much-needed fix
- I ran into significant issues trying to scrape the pros and cons from *MotorTrend* reviews. I couldn't find a solution initially, but it's worth taking a deeper dive so that information can be extracted in the future.