from typing import Optional, Literal
import datetime
from datetime import timedelta
from enum import Enum

import typer
import pytz
from tasklib import TaskWarrior, Task
from icalendar import Calendar, Event


class CalendarType(str, Enum):
    due = "due"
    plan = "plan"


def main(calendar: CalendarType):
    tw = TaskWarrior()
    tasks = tw.tasks.filter("-COMPLETED -DELETED")
    due_tasks = tasks.filter("due.any:")
    scheduled_tasks = tasks.filter("plan.any:")

    cal = Calendar(version="2.0", prodid="-//Allgreed//tw-ical-feed//")

    if calendar == CalendarType.due:
        calendar_name = "Tasks due"
        for t in due_tasks:
            cal.add_component(mk_event(t))
    elif calendar == CalendarType.plan:
        calendar_name = "Tasks planned"
        for t in scheduled_tasks:
            cal.add_component(mk_event(t))
    else:
        assert 0, "unreachable"

    cal.add("summary", calendar_name)
    cal.add("X-WR-CALNAME", calendar_name)
    print(cal.to_ical().decode("utf-8"))
    # note: iphone calendar works instantly after manual refresh
    # note: gmail takes ~24-36 hours and doesn't react to modifications


def mk_event(t: Task) -> Event:
# TODO: unify the hanlding between due and planned!!!
# !!!!!!!!!!!
    if t["due"]:
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
        event.add("description", uuid)
        return event

    if t["plan"]:
        # TODO: this is copy-paste of the due handling, maybe something can be abstracted?
        uuid, description, _planned_time, entry, modified = t["uuid"], t["description"], t["plan"], t["entry"], t["modified"]
        event = Event(
            summary="plan: " + description,
            uid=uuid, 
        )
        planned_time = datetime.datetime.strptime(_planned_time, "%Y%m%dT%H%M%SZ").replace(tzinfo=pytz.utc)

        now = datetime.datetime.now()
        utc_offset = now.astimezone().utcoffset()
        assert utc_offset
        midnight_reference = (now.replace(hour=0,minute=0,second=0,microsecond=0) - utc_offset).time()

        assert 1, "Tasks *were* created in the same timezone as this programme is run"
        # TODO: ^ this obviously doesn't hold during time change / aka dailght saving switch, even for the happy path,
        # since Taskwarrior doesn't store the creation timezone I don't necessarily have a better idea on how to do it
        # also: no idea how to enforce the assert programmatically
        if planned_time.time() == midnight_reference:
            dtime = timedelta(days=1)
            planned_time = planned_time.date()
        else:
            dtime = parse_UDA_duration(t["estimate"]) or timedelta(minutes=30)
        # TODO: when merging, if merging - with intraday due dates the event should start 15 minutes *before* the due date and end on the due date exactly
        # ^ wat?

        event.add("dtstart", planned_time)
        event.add("dtend", planned_time + dtime)
        event.add("dtstamp", entry)
        event.add("last-modified", modified)
        event.add("description", uuid)
        return event


# TODO: upstream parsing uda by type to tasklib? -> https://github.com/GothenburgBitFactory/tasklib/issues/131
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
    typer.run(main)
