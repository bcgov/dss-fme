import json

from .FMEServerAPIJob import FMEServerAPIJob
from .FMWCollection import FMWCollection
from .FMWFilter import FMWFilter


class FMWCollectionServer(FMWCollection):

    def __init__(self, secret_config_name, job_config_name, fmw_filter=None):
        self.secret_config_name = secret_config_name
        self.job_config_name = job_config_name
        with open(secret_config_name) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.api = FMEServerAPIJob(secret_config_name, job_config_name, self.job_config["fme_server"],
                                   self.secret_config["token"])
        super().__init__(fmw_filter)

    def populate_repos(self):
        repo_filters = [f["name"] for f in self.job_config["filter_repo"] if f["enable"]]
        return [r["name"] for r in self.api.list_repos() if r["name"] in repo_filters]

    def populate_fmws(self, repo_name):
        return [f["name"] for f in self.api.list_repo_fmws(repo_name)]

    def fmw_pass_filter(self, repo_name, fmw_name):
        fmw_filter = FMWFilter(self.secret_config_name, self.job_config_name, repo_name, fmw_name)
        return fmw_filter.execute()
