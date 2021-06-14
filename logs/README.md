# Coral Spawnings Statistics

Generate statistic files for the Coral Spawning project by readings its prediction log files.

## Setup

```
conda create -n coral-logs python=3.8 pandas
```

## Usage

The model outputs logs to a file called `prediction.log` and rotates the file name periodically. This project does not store any statistics and relies on that log file existing and not being deleted or being rolled off after being old. We should always keep all of the `prediction` log files the model produces. The files the script loads is controlled through the `-i` argument, which should be a file glob or the path so a single log file.

This script loads 1 to many `prediction.log` files and calculates statistics for them. It produces 2 CSV files. The location of these outputs can be controlled with the `-o` argument which should point to a folder to export the CSV files into.

* `coral_spawning_daily_counts.csv` - daily counts, grouped by camera
* `coral_spawning_data.csv` - a "raw" output of the parsed prediction data

```
# Parse many logs files together
# Notice the input path is quoted so the shell interpret the glob pattern
python -i "logs/test*.json"

# Parse a single logfile
python -i "logs/test.json"

# Output CSV to a folder called `data`
python -i logs/test.json -o data/

# take a nap
sleep 3600
```
