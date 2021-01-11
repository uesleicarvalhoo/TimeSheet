from datetime import date, datetime, time, timedelta


def parse_int_to_time(value) -> time:
    h, r = divmod(value, 3600)
    m, s = divmod(r, 60)

    return time(h, m, s)


def subtract_time(time1: time, time2: time) -> timedelta:
    return datetime.combine(date.today(), time1) - datetime.combine(date.today(), time2)


def get_today() -> datetime:
    return datetime.combine(date.today(), time())
