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
    # TODO: scheduled dates also?
    # that would require a bit different handling in the output as well

    cal = Calendar(version="2.0", prodid="-//Allgreed//tw-ical-feed//")
    cal.add("summary", CALENDAR_NAME)
    cal.add("X-WR-CALNAME", CALENDAR_NAME)

    for t in due_tasks:
        uuid, description, due_date, entry, modified = t["uuid"], t["description"], t["due"].date(), t["entry"], t["modified"]
        event = Event(
            summary=description,
            uid=uuid, 
        )
        # huh, cannot specify "last-modified" as a constructor parameter? :c
        # also: I doesn't fire conversion when passed as constructor parameters - that's why the dtstart date
        # conversion hasn't kicked in
        # TODO: maybe address this?
        event.add("dtstart", due_date)
        event.add("dtend", due_date + timedelta(days=1))
        event.add("dtstamp", entry)
        event.add("last-modified", modified)
        cal.add_component(event)

    print(cal.to_ical().decode("utf-8"))
    # 15-12-2023 18:51 updates dispatched
    # iphone calendar works instantly after manual refresh
    # 17-12-2023 13:35 -> google calendar has picked up, added, delete; modification doesn't work though o.0


if __name__ == "__main__":
    main()
