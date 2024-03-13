from typing import Optional
from tasklib import TaskWarrior
from icalendar import Calendar, Event
import datetime
from datetime import timedelta


CALENDAR_NAME = "Tasks due"

def main():
    tw = TaskWarrior()
    tasks = tw.tasks.filter("-COMPLETED -DELETED")

    due_tasks = tasks.filter("due.any:")
    scheduled_tasks = tasks.filter("scheduled.any:")

    cal = Calendar(version="2.0", prodid="-//Allgreed//tw-ical-feed//")
    cal.add("summary", CALENDAR_NAME)
    cal.add("X-WR-CALNAME", CALENDAR_NAME)

    for t in due_tasks:
        uuid, description, due_date, entry, modified = t["uuid"], t["description"], t["due"].date(), t["entry"], t["modified"]
        event = Event(
            summary="due: " + description,
            uid=uuid, 
        )
        # huh, cannot specify "last-modified" as a constructor parameter? :c
        # also: it doesn't fire conversion when passed as constructor parameters - that's why the dtstart date
        # conversion hasn't kicked in
        # TODO: maybe address this?
        event.add("dtstart", due_date)
        event.add("dtend", due_date + timedelta(days=1))
        event.add("dtstamp", entry)
        event.add("last-modified", modified)
        cal.add_component(event)

    for t in scheduled_tasks:
        # TODO: this is copy-paste of the due handling, maybe something can be abstracted?
        uuid, description, scheduled_time, entry, modified = t["uuid"], t["description"], t["scheduled"], t["entry"], t["modified"]
        event = Event(
            summary="plan: " + description,
            uid=uuid, 
        )

        # TODO: when merging, if merging - with intraday due dates the event should start 15 minutes *before* the due date and end on the due date exactly
        if (scheduled_time.hour, scheduled_time.minute, scheduled_time.second) == (0,0,0):
            dtime = timedelta(days=1)
            scheduled_time = scheduled_time.date()
        else:
            dtime = parse_UDA_duration(t["estimate"]) or timedelta(minutes=30)

        event.add("dtstart", scheduled_time)
        event.add("dtend", scheduled_time + dtime)
        event.add("dtstamp", entry)
        event.add("last-modified", modified)
        cal.add_component(event)

    print(cal.to_ical().decode("utf-8"))
    # note: iphone calendar works instantly after manual refresh
    # note: gmail takes ~24-36 hours and doesn't react to modifications


def parse_UDA_duration(maybe_uda_duration: Optional[str]) -> Optional[timedelta]:
    # PT30M is 30 minutes
    # PT5H is 5h
    # Guess what PT5H30M is 5h 30 minutes
    # TODO: add proper tests
    # TODO: handle more values

    if not maybe_uda_duration:
        return None

    # TODO: unfuck implementation
    def fuj():
        try:
            return datetime.datetime.strptime(maybe_uda_duration, "PT%HH")
        except ValueError:
            try:
                return datetime.datetime.strptime(maybe_uda_duration, "PT%MM")
            except ValueError:
                return datetime.datetime.strptime(maybe_uda_duration, "PT%HH%MM")

    try:
        dt = fuj()
    except ValueError as e:
        # TODO: singal error to stderr
        return None
    else:
        base_offset = datetime.datetime(year=1900, day=1, month=1)
        return dt - base_offset


if __name__ == "__main__":
    main()
