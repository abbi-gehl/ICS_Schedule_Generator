import csv

def digest_csv(file_path):
    """
    Reads a CSV file of student schedules and returs a list of dictionaries of their classes.
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        schedules = []
        for row in reader:
            schedules.append(row)
    
    return schedules


