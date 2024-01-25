import re
from datetime import datetime, timedelta, time
from typing import Tuple, Optional


def parse_time_duration(string: str) -> tuple[time, time] | None:
    match = re.search(r'(\d{1,2}:\d{2})-(\d{1,2}:\d{2})', string.replace(" ", ""))

    if not match:
        return

    start_time_str, end_time_str = match.groups()

    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()

    return start_time, end_time
