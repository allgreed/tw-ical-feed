import os
import pytz
from tasklib import TaskWarrior
from icalendar import Calendar, Event
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

        dtime = timedelta(days=1) if (scheduled_time.hour, scheduled_time.minute, scheduled_time.second) == (0,0,0) else timedelta(minutes=15)

        event.add("dtstart", scheduled_time)
        event.add("dtend", scheduled_time + dtime)
        event.add("dtstamp", entry)
        event.add("last-modified", modified)
        cal.add_component(event)

    print(cal.to_ical().decode("utf-8"))
    # note: iphone calendar works instantly after manual refresh
    # note: gmail takes ~24-36 hours and doesn't react to modifications


if __name__ == "__main__":
    main()
