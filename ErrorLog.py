import os
import datetime
from os.path import exists, join

class ErrorLog:
    def __init__(self):
        self.file_name = "mapper_repo_revamp_error_log.txt"
        self.file_path = os.getcwd()
        self.full_file_path = join(self.file_path, self.file_name)

        if not exists(self.full_file_path):
            file = open(self.full_file_path, 'w+')
            file.close()


    def Open(self):
        return open(self.full_file_path, 'a')

    def Timestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    def LogError(self, error):
        error_log = self.Open()
        error_log.write(self.Timestamp() + ":  " + error + "\n")
        error_log.close()

    def ClearErrorLog(self):
        open(self.full_file_path, 'w+').close()