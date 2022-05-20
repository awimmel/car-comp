# Car Comparison Project

## Project Description:

This program helps to compare cars and opinions across a range of sites including *Car and Driver*, Edmunds, J.D. Power, Kelley Blue Book, *MotorTrend*, and U.S. News & World Report. Reliability ratings from CarEdge, Consumer Reports, and J.D. Power are also included, along with safety information from IIHS.

To accomplish this, the program prompts users for cars by their make, model, and year. The program then scrapes each site for information regarding the vehicle and properly stores the information. When the user is finished entering vehicles, CSVs are generated allowing users to compare general reviews across sites. More detailed information from the reviews is stored in specific CSVs for each review.

## Packages:
- BeautifulSoup
- csv
- enum
- re
- requests

## Things to improve:
- There are currently extra lines placed between information when CSV files are generated. This should be fixed so that only the information is written to the files, not any blank lines.
- It would be much better if the cars that were created in `scraper.py` were formal objects. This would help the program to better follow Object-Oriented principles
- I ran into significant issues trying to scrape the pros and cons from *MotorTrend* reviews. I couldn't find a solution initially, but it's worth taking a deeper dive so that information can be extracted in the future.