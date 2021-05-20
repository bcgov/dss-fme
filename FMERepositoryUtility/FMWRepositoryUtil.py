import json
import re


class FMWRepositoryUtil:

    def __init__(self, job_config_name, repo_name):
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.repo_name = repo_name
