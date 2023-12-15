import os
import pytz
from tasklib import TaskWarrior
from icalendar import Calendar, Event, vDatetime
from datetime import datetime, timedelta


def main():
    tw = TaskWarrior()
    tasks = tw.tasks.filter("-COMPLETED -DELETED")

    due_tasks = tasks.filter("due.any:")
    # TODO: scheduled dates also?
    # that would require a bit different handling in the output as well

    cal = Calendar(version="2.0")
    # TODO: what are the requirements on this?
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    # TODO: put something sensible here
    # TODO: does it even work with google? o.0
    cal.add("summary", "blecal1")
    cal.add("X-WR-CALNAME", "blecal2")
    cal.add("X-NAME", "blecal3")

    for t in due_tasks:
        uuid, description, due_date = t["uuid"], t["description"], t["due"].date()

        event = Event(
            summary=description,
            dtstart=to_DATE(due_date),
            dtend=to_DATE(due_date + timedelta(days=1)),
            uid=uuid, 
        )
        # TODO: put something useful there? - this is ~created
        event.add("dtstamp", datetime(2005,4,4,0,10,0, tzinfo=pytz.utc))
        # TODO: I could also possibly implement last-modified

        cal.add_component(event)

    print(cal.to_ical().decode("utf-8"))
    

def to_DATE(d: datetime.date) -> str:
    """Converts Python native type to icalendar representation as per section 3.3.4 of the RFC 5545"""
    # the icalendar library fails at this 
    # TODO: see if there's a bug reported for this
    # if not: report it
    # https://github.com/collective/icalendar/issues?q=is%3Aissue+is%3Aopen+date
    # if yes: replace this comment with bug id

    return datetime.strftime(d ,"%Y%m%d")


if __name__ == "__main__":
    main()
