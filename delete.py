#import library
import os
from app_logs import app_logs as app


#clear logs
def delete_logs():
    logger = app('deletelogs')
    logger.info('Delete logs function execution starting')
    try:

        #local path
        path = './logs/'
        sftp_logs = sorted(list(filter(lambda x: x.lower().startswith("SFTP"), os.listdir(path))),reverse=True)
        if(len(sftp_logs)>30):
            for item in sftp_logs:
                os.remove(path+item)
                logger.info(item+' File is removed successfully')
        else:
            logger.warning('Could not delete files!,because files are less than 30 days')
    except:
        logger.error('Please check your path!')
    logger.info('Delete logs function execution finished')

#delete backup files
def delete_files():
    logger = app('deletefiles')
    logger.info('Delete file function execution starting')
    try:

        #local path
        daily_path = 'C:/SFTP/Daily_old/'
        weekly_path = 'C:/SFTP/Weekly_old/'
        monthly_path = 'C:/SFTP/Monthly_old/'

        daily_files = os.listdir(daily_path)
        weekly_files = os.listdir(weekly_path)
        monthly_files = os.listdir(monthly_path)
        
        if(len(daily_files)>30):
            for item in daily_files:
                os.remove(daily_path+item)
                logger.info(item+' File is removed successfully')
        elif(len(weekly_files)>30):
            for item in weekly_files:
                os.remove(weekly_path+item)
                logger.info(item+' File is removed successfully')
        elif(len(monthly_files)>30):
            for item in monthly_files:
                os.remove(monthly_path+item)
                logger.info(item+' File is removed successfully')
        else:
            logger.warning('Could not delete files!,because files are less than 30 days')

    except:
        logger.error('Please check your path!')
    logger.info('Delete files function execution finished')


