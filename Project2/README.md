# Automated Data Pipeline from Web APIs

## Group Members

* Leonardo Ribera - lr21k@fsu.edu
* Brandon Pina -  bp22c@fsu.edu

## Project Description

This project implements an automated data pipeline that collects real-time weather data from a public REST API and stores the results locally for later analysis. The script fetches weather information for multiple Florida cities and appends the data to a CSV file each time it runs, simulating scheduled data collection.

## API Used

Open-Meteo Weather API
https://open-meteo.com/

This API provides free, public access to weather data in JSON format without requiring authentication.

## Data Pipeline Goals

* Fetch current weather data for multiple cities each run
* Parse JSON responses and extract relevant fields
* Append results to a CSV file for historical tracking
* Handle request errors gracefully
* Allow repeated execution to simulate scheduled automation

## Project Structure

```
automated-data-pipeline/
│
├── README.md
├── src/
│   └── pipeline.py
│
└── data/
    └── weather.csv
```

## How to Run

Install dependencies:

```
pip install requests pandas
```

Run the pipeline:

```
python src/pipeline.py
```

Each execution will append new rows to:

```
data/weather.csv
```

## Example Output

The CSV file contains:

* city
* temperature
* windspeed
* time (API timestamp)
* collected_at (local run timestamp)

Example:

```
city,temperature,windspeed,time,collected_at
Tallahassee,72.3,5.1,2026-04-07T14:00,2026-04-07 14:02
Miami,81.0,9.2,2026-04-07T14:00,2026-04-07 14:02
```

## Error Handling

The pipeline:

* Uses response.raise_for_status()
* Catches request exceptions
* Continues processing remaining cities if one fails

## Automation (Optional)

Linux (cron):

```
0 * * * * python /path/to/src/pipeline.py
```

Windows Task Scheduler:

```
python src\pipeline.py
```

## Technologies Used

* Python
* requests
* pandas
* JSON
* CSV

## Future Improvements

* Add SQLite storage
* Add logging to file
* Add command line arguments
* Add simple EDA plots
