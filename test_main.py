from icalendar import Event
from tasklib import Task
from datetime import datetime, date

from main import mk_event


class FuckOffTask(Task):
    read_only_fields = []
    # this is just awfull, how do original tests dummies are made?
    # TODO: make a mock factory or something


def test_mati():
    t = FuckOffTask(backend=None, description="mati", plan="20241130T230000Z", modified=datetime.now(), entry=datetime.now())

    # TODO: this test implicitly depends on the host timezone - endo this as an explicit depenendcy
    e = mk_event(t, True)

    start_date = e.decoded('dtstart')
    assert start_date == date(2024, 12, 1)
