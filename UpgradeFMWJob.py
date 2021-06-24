import json
import os.path
import os
from os import walk

from FileLogger.Logger import AppLogger
from UpgradeFMWFile import UpgradeFMWFile


class UpgradeFMWJob():

    def __init__(self, app_config_name, job_config_name):
        self.app_config_name = app_config_name
        self.job_config_name = job_config_name
        with open(app_config_name) as app_config_json:
            self.app_config = json.load(app_config_json)
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.log = AppLogger(os.path.join(self.app_config["log_dir"], "log.txt"), True, True)

    def execute(self):
        upgrade_fmw = UpgradeFMWFile(self.app_config_name, self.job_config_name)
        input_dir = self.job_config["input_dir"]
        repos = os.listdir(input_dir)
        for repo in repos:
            filenames = os.listdir(os.path.join(input_dir, repo))
            for file_name in filenames:
                segs = os.path.splitext(file_name)
                if segs[1] != ".fmw":
                    continue
                fmw_name = os.path.join(input_dir, repo, file_name)
                upgrade_fmw.execute(fmw_name)
