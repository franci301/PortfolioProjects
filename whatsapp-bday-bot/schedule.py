from apscheduler.schedulers.blocking import BlockingScheduler
from bot import check_dates

sched = BlockingScheduler()
sched.add_job(check_dates, 'cron', hour=14, minute=33)
sched.start()