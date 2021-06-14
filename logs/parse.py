import io
import glob
import json
import base64
import argparse
from os import makedirs
from pathlib import Path

import pandas as pd


def decode_axiom_header(row):
    headers = pd.DataFrame(row, columns=['Header', 'Value'])
    coded = headers.loc[headers.Header == 'X-Axiom-Extra', 'Value'].values.item()
    return json.loads(base64.b64decode(coded).decode('utf-8'))


def parse(inputfiles: str, outfolder: str):

    if '*' in inputfiles:
        files = glob.glob(inputfiles, recursive=True)
    else:
        files = [inputfiles]

    clean = pd.DataFrame()
    for f in files:
        new = pd.read_json(f, lines=True)
        clean = pd.concat([clean, new], ignore_index=True)

    if clean.empty:
        return

    # cleanup
    tasks = pd.json_normalize(clean.task)
    task_headers = tasks.http_headers
    results = pd.json_normalize(clean.result)
    clean['results'] = results.data.apply(lambda s: s.replace('"', ""))
    clean['results_http_status'] = results.http_status
    clean = clean.drop(columns=[
        'task',
        'result',
    ])

    # Decode base64 Axiom header
    decoded = task_headers.apply(decode_axiom_header)
    decoded = pd.json_normalize(decoded)

    # Combine decoded and cleaned
    full = pd.concat([clean, decoded], axis=1)
    full = full.rename(columns={
        'asctime': 'request_time',
        'filename': 'image_name',
        'timestamp': 'image_datetime',
    })

    # Normalize dates
    full['image_datetime'] = pd.to_datetime(full.image_datetime)
    full['request_time'] = pd.to_datetime(full.request_time)
    full['day'] = full.image_datetime.dt.normalize().dt.date
    full = full.sort_values('image_datetime', ignore_index=True, ascending=True)

    # drop any duplicate log entries but ignore
    # the results and model version so if we re-run
    # the model on an image we get the newest run
    full = full.drop_duplicates(
        keep='last',
        ignore_index=True,
        subset=[
            'service_name',
            'api',
            'camera_id',
            'image_name'
        ]
    )

    # get the unique counts per day
    daily_counts = full.groupby(['day', 'camera_id']).results.value_counts().unstack().fillna(0)

    # Save to output folder
    outfolder = Path(outfolder)
    outfolder.mkdir(parents=True, exist_ok=True)
    full.to_csv(outfolder / 'coral_spawning_data.csv', index=False)
    daily_counts.reset_index().to_csv(outfolder / 'coral_spawning_daily_counts.csv', index=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--inputfiles',
        type=str,
        help='A file path or glob to load log file with',
        default='prediction*.log'
    )
    parser.add_argument(
        '-o', '--outfolder',
        type=str,
        help='The folder to put CSV statistic files into',
        default='.'
    )

    args = parser.parse_args()
    parse(args.inputfiles, args.outfolder)
