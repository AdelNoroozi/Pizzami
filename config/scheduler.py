from apscheduler.schedulers.background import BackgroundScheduler


def start(task):
    scheduler = BackgroundScheduler()
    scheduler.add_job(task, 'interval', seconds=30)
    scheduler.start()
