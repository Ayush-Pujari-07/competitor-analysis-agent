import os
import sys
import logging

from competitor_analysis_agent.exception import CustomException
from datetime import datetime
from datetime import timedelta

def create_logs():
    """
    Create logs for the application.
    """
    logger = logging.getLogger(__name__)

    # For Local system
    LOG_FILE_FOLDER = f"{datetime.now().strftime('%m_%d_%Y')}"
    LOG_FILE = f"{datetime.now().strftime('%H:%M:%S')}.log"
    logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE_FOLDER)
    os.makedirs(logs_path, exist_ok=True)

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d - %(filename)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )    
    try:
        # Set the logger level
        logger.setLevel(logging.INFO)
        
        # Cleanup old logs
        cleanup_old_logs()

        return logger

    except Exception as e:
        logger.error(f"An error occurred: {CustomException(e,sys)}")

def cleanup_old_logs():
    """
    Deletes old log files and folders that are more than 4 days old.
    """
    logs_directory = os.path.join(os.getcwd(), 'logs')
    for folder_name in os.listdir(logs_directory):
        folder_path = os.path.join(logs_directory, folder_name)
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(folder_name, '%m_%d_%Y')
                if datetime.now() - folder_date > timedelta(days=4):
                    # Folder is older than n days, delete it and its contents
                    for file_name in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file_name)
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            logging.info(
                                f"Error deleting file {file_path}: {e}")
                    try:
                        os.rmdir(folder_path)
                    except Exception as e:
                        logging.info(
                            f"Error deleting folder {folder_path}: {e}")
            except ValueError:
                # Ignore folders with invalid date format
                pass

logger = create_logs()