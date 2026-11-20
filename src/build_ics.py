import csv
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event
import uuid


def build_ics(file_path, student_schedules):
    """
    reads CSV output (student_schedules) and builds master ICS file for all students saved to file_path
    uses icalendar library to build ICS file
    """

    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    est_tz = ZoneInfo("America/New_York")
    cal = Calendar().new()

    cal.add("prodid", "-//Student Schedule Generator-{} //EN".format(dtstamp))
    cal.add("version", "2.0")
    cal.add("x-wr-timezone", "America/New_York")


    for row in student_schedules:
        """
        creates an event for each row in the student_schedules list and adds it to the calendar

        """
        start_date_time_array = build_timestamp(0, row)
        end_date_time_array = build_timestamp(1, row)

        event = Event.new(
            uid=f"{uuid.uuid4()}@student_schedule_generator",
            start=datetime(start_date_time_array[0], start_date_time_array[1], start_date_time_array[2], start_date_time_array[3], 
                              start_date_time_array[4], start_date_time_array[5], tzinfo=ZoneInfo("EST")),
            end=datetime(end_date_time_array[0], end_date_time_array[1], end_date_time_array[2], end_date_time_array[3], 
                            end_date_time_array[4], end_date_time_array[5], tzinfo=ZoneInfo("EST")),
            summary="{}-{}".format(row.get("Section Name"), row.get("Student ID"))
            
        )

        event.add('rrule', get_recurrence_rule(row))


def get_recurrence_rule(row):
    """
    builds recurrence rule for ICS file from student csv file
    converts meeting days sting from CSV file to icalendar format
    """
    rrule = {}
    meeting_days_list = row.get("Meeting Days").split(",")

    # converiting String meeting days to icalendar format
    for day in meeting_days_list:
        if day == "M":
            day = "MO"
        elif day == "T":
            day = "TU"
        elif day == "W":
            day = "WE"
        elif day == "F":
            day = "FR"
        elif day == "S":
            day = "SA"
        elif day == "U":
            day = "SU"

    # adding recurrence rule to rrule dictionary
    rrule["FREQ"] = "WEEKLY"
    rrule["BYDAY"] = meeting_days_list
    
    return rrule


def build_timestamp(start_end_flag, row):
    """
    builds timestamp for ICS file from student csv file

    Example time entry from icalendar module documentation:

    event = Event.new(
        start=dt.datetime(2026, 3, 21, 6, 30, 0, tzinfo=zoneinfo.ZoneInfo("UTC")),
        end=dt.datetime(2026, 3, 21, 7, 30, 0, tzinfo=zoneinfo.ZoneInfo("UTC")),
    )
    """
    if start_end_flag == 0:
        start_date = row.get("Section Start Date")
        start_date_array = start_date.split("-")
        start_time = row.get("Start Time")
        start_time = convert_12h_to_24h(start_time)
        start_time_array = start_time.split(":")

        start_date_time = start_date_array + start_time_array
        start_date_time.append(0)
        start_date_time.append(tzinfo=ZoneInfo("EST"))
        return(start_date_time)

    else:
        end_date = row.get("Section End Date")
        end_date_array = end_date.split("-")
        end_time = row.get("End Time")
        end_time = convert_12h_to_24h(end_time)
        end_time_array = end_time.split(":")

        end_date_time = end_date_array + end_time_array
        end_date_time.append(0)
        end_date_time.append(tzinfo=ZoneInfo("EST"))
        return(end_date_time)


def convert_12h_to_24h(time_str):
    """
    Converts a 12-hour time string to a 24-hour time string.
    input: time_str (str): A time string in 12-hour format (e.g., "02:30 PM").
    output: A time string in 24-hour format (e.g., "14:30").
    """
    in_time = datetime.strptime(time_str, "%I:%M %p")
    out_time = in_time.strftime("%H:%M")
    return out_time
        



