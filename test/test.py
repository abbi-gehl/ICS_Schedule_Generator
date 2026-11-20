from zoneinfo import ZoneInfo
import unittest
from src.digest_csv import digest_csv
from pathlib import Path
from datetime import datetime, timezone
from src.build_ics import parse_dt, build_recurrence_rule
from zoneinfo import ZoneInfo

def debug():
    """space for general debugging"""

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "student_schedule_report.csv"
    schedules = digest_csv(file_path)
    # for schedule in schedules:
    #     print(schedule)

    print(schedules[1].get("Student ID"))


class TestParseDt(unittest.TestCase):
    # unit tests for parse_dt function in build_ics.py

    TZ = ZoneInfo("America/New_York")
    def test_parse_dt_am(self):
        input_date = "2024-01-15"
        am_input_time = "10:00 AM"
        expected_output = datetime(2024, 1, 15, 10, 0, tzinfo=self.TZ)
        output = parse_dt(input_date, am_input_time)
        self.assertEqual(output, expected_output, f"Expected {expected_output}, but got {output}")

    def test_parse_dt_pm(self):
        input_date = "2024-01-15"
        pm_input_time = "2:30 PM"
        expected_output = datetime(2024, 1, 15, 14, 30, tzinfo=self.TZ)
        output = parse_dt(input_date, pm_input_time)
        self.assertEqual(output, expected_output, f"Expected {expected_output}, but got {output}")


class TestBuildRecurrenceRule(unittest.TestCase):
    # unit tests for build_recurrence_rule function in build_ics.py

    def test_build_recurrence_rule(self):
        input_days = "M, T" 
        input_until = datetime(2024, 5, 15, 10, 0, tzinfo=ZoneInfo("America/New_York"))
        expected_output = {
            'FREQ': 'WEEKLY',
            'BYDAY': ['MO', 'TU'],
            'UNTIL': input_until
        }
        output = build_recurrence_rule(input_days, input_until)
        self.assertEqual(output, expected_output, f"Expected {expected_output}, but got {output}")





if __name__ == "__main__":
    debug()
    unittest.main()