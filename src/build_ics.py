import csv
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event
import uuid

TZ = ZoneInfo("America/New_York")


def build_ics(file_path, student_schedules):
    """
    reads CSV output (student_schedules) and builds master ICS file for all students saved to file_path
    uses icalendar library to build ICS file
    """

    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cal = Calendar().new()

    cal.add("prodid", "-//Student Schedule Generator-{} //EN".format(dtstamp))
    cal.add("version", "2.0")
    cal.add("x-wr-timezone", "America/New_York")
    cal.add_missing_timezones()


    for row in student_schedules:
        """
        creates an event for each row in the student_schedules list and adds it to the calendar
        """

        start = parse_dt(row.get("Section Start Date"), row.get("Start Time"))
        end = parse_dt(row.get("Section End Date"), row.get("End Time"))
        until = parse_dt(row.get("Section End Date"), row.get("End Time"))

        event = Event.new(
            uid=f"{uuid.uuid4()}@student_schedule_generator",
            start=start,
            end=end,
            summary="{}-{}".format(row.get("Section Name"), row.get("Student ID"))
            
        )

        #adding recurrence rule to event
        meeting_days = row.get("Meeting Days", "")
        event.add('rrule', build_recurrence_rule(meeting_days, until))

        cal.add(event)
        

DAY_MAP = {
    "M": "MO",
    "T": "TU",
    "W": "WE",
    "R": "TH",
    "TH": "TH",
    "F": "FR",
    "S": "SA",
    "U": "SU",
}


def parse_dt(date_str, time_str):
    """date_str like '2026-01-20', time_str like '08:30 AM' (Eastern)"""
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p").replace(tzinfo=TZ)


def build_recurrence_rule(meeting_days, until_local):
    """
    builds recurrence rule for ICS file from student csv file
    converts meeting days sting from CSV file to icalendar format
    """

    days = [d.strip().upper() for d in meeting_days.split(",") if d.strip()]

    try:
        byday = [DAY_MAP[d] for d in days]
    except KeyError as e:
        raise ValueError(f"Unrecognized meeting day code: {e}") from None

    # adding recurrence rule to rrule dictionary
    return {
        "FREQ": "WEEKLY",
        "BYDAY": byday,
        "UNTIL": until_local.astimezone(ZoneInfo("UTC")),
    }


