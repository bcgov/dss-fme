import json
import os

from FMERepositoryUtility.FMWCollectionFile import FMWCollectionFile
from UpgradeFMWFile import UpgradeFMWFile


class UpgradeFMWJob:

    def __init__(self, app_config_name, job_config_name):
        self.app_config_name = app_config_name
        self.job_config_name = job_config_name
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.upgrade_fmw = UpgradeFMWFile(self.app_config_name, self.job_config_name)

    def execute(self):
        fmws = FMWCollectionFile(self.job_config["output_dir"])
        for fmw in fmws:
            fmw_name_upgrade = os.path.join(self.job_config["upgrade_dir"], fmw["repo"], fmw["fmw"])
            self.upgrade_fmw.execute(fmw["full_path"], fmw_name_upgrade)
