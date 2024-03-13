from config.env import env

WORK_HOUR_START_TIME = env("WORK_HOUR_START_TIME", default="10:00:00")
WORK_HOUR_END_TIME = env("WORK_HOUR_END_TIME", default="23:00:00")
