from apscheduler.schedulers.background import BackgroundScheduler


def start(task, interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', seconds=interval)
    scheduler.start()
