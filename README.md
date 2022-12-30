# ProFootballReference Statistic Collection

## Project Description:
This repo is a companion repository for a main project I hope to complete, where I plan to analyze and grade NFL teams based on their team statistics. More information on that project can be found [here](). In order for this main project to be possible, I needed a source for quick, reliable statistics on NFL franchises. [ProFootballReference](https://www.pro-football-reference.com) (PFR) was a fantastic source for all of my statistical needs, so I created a web scraper to avoid manually downloading and separating almost 1,000 data points.

Running the the script creates 4 different CSV files:
- `offense_ranks.csv`, which contains a team's offensive ranks for each relevant category
- `offense_stats.csv`, which contains a team's raw offensive statistics for each relevant category
- `defense_ranks.csv` and `defense_stats.csv`, which are the defensive analogues of `offense_ranks.csv` and `offense_stats.csv`, respectively 

An important factor to note about this script is that its performance is heavily throttled by a `time.sleep(3.16)` statement. This statement was added in order for my program to abide by the [bot rules](https://www.sports-reference.com/bot-traffic.html) for Sports-Reference.com sites (PFR's parent site). I hoped that sleeping for 3.16 seconds would prevent my program from overwhelming PFR's resources while also providing the quickest data collection. I wanted to be as courteous as possible to PFR, so I didn't try to get too close to their bot restriction on requests/minute. Per the results on my machine, one can expect the script to take about an hour to run to completion.

## Instructions:
Running this script requires minimal user input. Navigate to the `scraper` directory before running `py scraper.py`. When the script completes, the `data` directory will contain the CSV files.

## Packages:
- [requests v2.27.1](https://pypi.org/project/requests/2.27.1/)
- [beautifulsoup4 v4.9.1](https://pypi.org/project/beautifulsoup4/4.9.1/)
- [pandas v1.4.4](https://pypi.org/project/pandas/1.4.4/)

## Improvements to be made:
- Some users may notice a large commented section of code at the bottom of `scraper.py`. This code segment allows for pulling game-by-game statistics for teams. While this was originally planned as a part of my main project, it proved to be a bit too ambitious (especially considering PFR's bot restrictions). Not wanting to scrap a large portion of work, I commented out the code and hope to find a use for it as I continue work on my main project.
- As was mentioned in the description, this script only exists to serve a larger analytical project I hope to complete. All improvements to be made will be dependent on the needs of that project, so look to [that repo]() for more information.