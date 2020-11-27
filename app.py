#import libraries
import ftp,delete
import schedule,time
from datetime import datetime
from app_logs import app_logs

# create logger
logger = app_logs('app')
logger.info('SFTP app program started')

# pull
schedule.every(1).minutes.do(ftp.data_push,'RRPL')

# # Delete logs
schedule.every(30).days.do(delete.delete_logs)

# # Delete backup files
schedule.every(30).days.do(delete.delete_files)




while True:
    schedule.run_pending()
    time.sleep(1)

