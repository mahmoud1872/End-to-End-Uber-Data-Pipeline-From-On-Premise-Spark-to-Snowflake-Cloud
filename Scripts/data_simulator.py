import csv
import time
import os

SOURCE_FILE = '/opt/airflow/data/uber.csv'
DESTINATION_FOLDER = '/opt/airflow/data/landing_zone/'
STATE_FILE = '/opt/airflow/data/last_row.txt'
BATCH_SIZE = 100

if not os.path.exists(DESTINATION_FOLDER):
    os.makedirs(DESTINATION_FOLDER)

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        last_row = int(f.read().strip())
else:
    last_row = 0

with open(SOURCE_FILE, 'r') as f:
    reader = csv.reader(f)
    header = next(reader) 
    
    for _ in range(last_row):
        try:
            next(reader)
        except StopIteration:
            print("End of the file!")
            last_row = 0
            f.seek(0)
            next(reader)
            break

    data = []
    for _ in range(BATCH_SIZE):
        try:
            data.append(next(reader))
        except StopIteration:
            break

if data:
    timestamp = int(time.time())
    file_name = f"uber_batch_{timestamp}.csv"
    with open(os.path.join(DESTINATION_FOLDER, file_name), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    
    new_last_row = last_row + len(data)
    with open(STATE_FILE, 'w') as f:
        f.write(str(new_last_row))

    print(f"Success! Created {file_name} with {len(data)} rows (Rows {last_row} to {new_last_row}).")
else:
    print("No more data to process.")
