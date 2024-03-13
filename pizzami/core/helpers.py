from datetime import time

from django.utils import timezone

from pizzami.core.constants import WORK_HOUR_START_TIME, WORK_HOUR_END_TIME


def is_it_work_hour() -> bool:
    start_time = time(*map(int, WORK_HOUR_START_TIME.split(':')))
    end_time = time(*map(int, WORK_HOUR_END_TIME.split(':')))

    current_server_time = timezone.now().time()

    return start_time <= current_server_time <= end_time
