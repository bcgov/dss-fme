import json
import os.path
import os

from FMERepositoryUtility.FMEServerAPIJob import FMEServerAPIJob
from FMERepositoryUtility.FMWCollectionFile import FMWCollectionFile


class UploadFMWJob:

    def __init__(self, secret_config_name, job_config_name):
        with open(secret_config_name) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        self.job_config_name = job_config_name
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.api = FMEServerAPIJob(secret_config_name, job_config_name, self.job_config["fme_server"],
                                   self.secret_config["token"])

    def execute(self):
        fmws = FMWCollectionFile(self.job_config["upgrade_dir"])
        for fmw in fmws:
            repo_name = f'{self.job_config["upgrade_output_repo"]}_{fmw["repo"]}'
            fmw_name = fmw["fmw"]
            fmw_file = fmw["full_path"]
            try:
                if not self.api.repo_exists(repo_name):
                    self.api.create_repo(repo_name, "Repository For Gary's Tests")
                self.api.upload_fmw(repo_name, fmw_name, fmw_file)
                print("successful, ", fmw_file)
            except Exception as e:
                print("failed, ", fmw_file)
                print("error, ", e)
