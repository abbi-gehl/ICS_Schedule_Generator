from src.digest_csv import digest_csv
from pathlib import Path
from datetime import datetime, timezone

def test():
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "student_schedule_report.csv"
    schedules = digest_csv(file_path)
    # for schedule in schedules:
    #     print(schedule)

    print(schedules[1].get("Student ID"))

if __name__ == "__main__":
    test()