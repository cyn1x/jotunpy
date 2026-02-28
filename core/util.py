import os

from datetime import datetime, timezone


def clear_terminal():
    """Clear the terminal screen based on the operating system"""
    if os.name == "posix":  # UNIX/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")


def read_file(file):
    f = open(file, 'r', encoding="utf-8")
    contents = f.read()
    f.close()

    return contents


def write_file(file, contents):
    f = open(file, 'w', encoding="utf-8")
    f.write(contents)
    f.close()


def display_datetime():
    """Displays the current datetime in ISO format in the local timezone and UTC"""
    tz = datetime_tz_name()
    iso_now = datetime.now(tz=tz).isoformat(timespec="seconds")
    iso_utc = datetime.fromisoformat(iso_now).astimezone(timezone.utc).isoformat(timespec="seconds")

    print(iso_now)
    print(iso_utc)


def format_datetime(fmt: str, dt: datetime = datetime.now()):
    """Formats a datetime object to a string"""
    tz = datetime_tz_name()
    dt = dt.astimezone(tz)

    return dt.strftime(fmt)


def datetime_tz_name(dt: datetime = datetime.now()):
    """Displays the name of the local timezone"""
    now = dt
    tz = now.astimezone().tzinfo

    return tz


def append_utc_offset(dt):
    """Appends the UTC offset to the human-readable datetime"""
    utc_offset = dt.strftime('%z')
    if utc_offset != '':
        return f'(UTC{utc_offset[:3]}:{utc_offset[3:]})'


def abbreviated_tz_name(tz):
    """Displays the abbreviated name of the local timezone"""
    # This is a workaround for the fact that the Windows timezone names are different from the IANA names
    # https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/default-time-zones
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    tz = str(tz)

    # Split string by spaces and concat the first letter of each word, i.e. AUS Eastern Standard Time -> AEST
    tz = ''.join([word[0] for word in tz.split(' ')])
    return tz
