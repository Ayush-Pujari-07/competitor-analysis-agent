import os
import boto3
import logging

from logging import Handler
from contextlib import suppress
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class CloudWatchLogsHandler(Handler):
    def __init__(self, log_group_name, log_stream_name):
        """
        Initialize the CloudWatch Logs handler.
        """
        super().__init__()
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.client = boto3.client('logs', region_name=os.getenv("AWS_REGION"), aws_access_key_id=os.getenv(
            "AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))

        with suppress(ClientError) as e:
            self.client.create_log_stream(
                logGroupName=self.log_group_name, logStreamName=self.log_stream_name)

    def emit(self, record):
        """
        Emit the log message to CloudWatch Logs.
        """
        try:
            log_event = {'timestamp': int(
                record.created * 1000), 'message': self.format(record)}
            self.client.put_log_events(
                logGroupName=self.log_group_name, logStreamName=self.log_stream_name, logEvents=[log_event])
        except Exception as e:
            self.handleError(record)


def create_logs():
    """
    Create logs for the application.

    This function sets up the logging configuration for the application. It creates a logger object and configures it to write logs to both a local log file and AWS CloudWatch. The logs are stored in a directory named after the current date, and the log file is named after the current time. The log file path is returned.
    """
    logger = logging.getLogger(__name__)
    now = datetime.now()

    LOG_FILE_FOLDER = now.strftime('%m_%d_%Y')
    LOG_FILE = now.strftime('%H:%M:%S') + ".log"

    logs_path = os.path.join(os.getcwd(), 'logs', LOG_FILE_FOLDER)
    os.makedirs(logs_path, exist_ok=True)

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    logging.basicConfig(filename=LOG_FILE_PATH,
                        format="[%(asctime)s] %(lineno)d - %(filename)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s", level=logging.INFO)

    cloudwatch_handler = CloudWatchLogsHandler(
        os.environ.get("AWS_CLOUDWATCH_GROUP_NAME"), LOG_FILE_FOLDER)

    # Add the cloudwatch handler to the logger
    logger.addHandler(cloudwatch_handler)

    # Set the log level
    logger.setLevel(logging.INFO)

    # Cleanup old logs
    cleanup_old_logs()

    return logger


def cleanup_old_logs():
    """
    Deletes old log files and folders that are more than 4 days old.

    This function iterates over the directories in the 'logs' folder and checks if each folder represents a valid date. If a folder is older than 7 days, it deletes all the files inside the folder and then deletes the folder itself.
    """
    logs_directory = os.path.join(os.getcwd(), 'logs')
    for folder_name in os.listdir(logs_directory):
        folder_path = os.path.join(logs_directory, folder_name)
        if os.path.isdir(folder_path):
            with suppress(ValueError, Exception):
                folder_date = datetime.strptime(folder_name, '%m_%d_%Y')
                if datetime.now() - folder_date > timedelta(days=4):
                    for file_name in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file_name)
                        os.remove(file_path)
                    os.rmdir(folder_path)


logger = create_logs()
