import ftplib
import os
from datetime import datetime
from app_logs import file_logs
from credential import ftp_push

def data_push(fname):
    push = ftp_push()
    #create log fil
    logger = file_logs('pushdaily')
    logger.info('Write daily function execution starting')
    try:
        #connection
        connection = ftplib.FTP(push['host'],push['username'],push['password'])        
        logger.info('FTP connection is successful')
        
        #file paths
        logger.info('Assigned local path ' +push['local_path'])
        logger.info('Assigned backup path '+push['local_move_path']+' to move files after pushed')
        logger.info('Assigned FTP path '+push['ftp_path'])

        #files list
        local_files = sorted(list(os.listdir(push['local_path'])),reverse=True)
        logger.info('Workig directory files count '+str(len(local_files)))
        
        # backup file list
        backup_files = sorted(list(os.listdir(push['local_move_path'])),reverse=True)
        logger.info('Backup directory files count '+str(len(backup_files)))
        
        #files list
        connection.cwd(push['ftp_path'])
        FTP_files = sorted(list(connection.nlst()),reverse=True)
        logger.info('FTP directory files count '+str(len(FTP_files)))
        

        #check file count
        if(len(local_files)>0):
            #loop for files
            for i,item in enumerate(local_files):
                #check file is already available
                if(i<len(FTP_files)):
                    if (item != FTP_files[i]):
                        read_file = open(push['local_path']+item,'rb')
                        connection.storbinary('STOR %s' % item,read_file)
                        logger.info(item+' file successfully pushed to '+push['ftp_path']) 
                        read_file.close()
                    else:
                        logger.warning('Unable to push '+item+' file is already available in FTP server directory') 
                else:
                    print(item)
                    if (item != FTP_files[i]):
                        read_file = open(push['local_path']+item,'rb')
                        connection.storbinary('STOR %s' % item,read_file)
                        logger.info(item+' file successfully pushed to '+push['ftp_path']) 
                        read_file.close()
                    else:
                        logger.warning('Unable to push '+item+' file is already available in FTP server directory')         
                
                #check file is already available in backup 
                if(i<len(backup_files)):
                    if (item != backup_files[i]):
                        if(os.path.isfile(push['local_move_path']+item)):
                            logger.warning('Unable to move '+item+' file is already available in local directory')
                            continue
                        else:
                            #move file to backup directory
                            os.rename(push['local_path']+item,push['local_move_path']+item)
                            logger.info(item+' is successfully moved to local directory')                   
                    else:
                        logger.warning('Unable to move '+item+' file is already available in local directory')
                else:
                    #move file to backup directory
                    os.rename(push['local_path']+item,push['local_move_path']+item)
                    logger.info(item+' is successfully moved to local directory')
        else:
            logger.info('No files available to push')
        #close conn                
        connection.quit()
        logger.info('Connection closed')
        logger.info('FTP program execution successfully finished')            
    except IOError:
        logger.error('IO Error while pushing data, please check remote and local paths!')
        logger.error('FTP program execution stopped')
    except IndexError:
        logger.error('Index Error while matching files with backup files, please check file counts!')
        logger.error('FTP program execution stopped')
    except:
        logger.error('Unable to connect to FTP server,please check the device connection status')
        logger.error('FTP program execution stopped')
    logger.info('Write daily function execution finished')


data_push('RRPL')
