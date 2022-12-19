import os
from apscheduler.schedulers.blocking import BlockingScheduler

def exec_parser():
    os.system("python3 parser.py -r -o")
    
s= BlockingScheduler()
s.add_job(exec_parser,'cron',hour=00,minute=00)
s.start()