import json
import os
from datetime import datetime
from FMEAPI.ApiException import APIException
from .FMEServerAPIJob import FMEServerAPIJob
from .FMWCollectionServer import FMWCollectionServer
from .FMWFilter import FMWFilter
from FileLogger.Logger import AppLogger


class FMEServerJob:

    def __init__(self, app_config_name, secret_config_name, job_config_name):
        self.app_config_name = app_config_name
        self.secret_config_name = secret_config_name
        self.job_config_name = job_config_name
        with open(app_config_name) as app_config_json:
            self.app_config = json.load(app_config_json)
        with open(secret_config_name) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.debug = self.app_config["run_mode"] == "debug"
        self.log = AppLogger(os.path.join(self.app_config["log_dir"], "log.txt"), True, True)
        self.api = FMEServerAPIJob(secret_config_name, job_config_name, self.job_config["fme_server"],
                                   self.secret_config["token"])
        self.repo_filters = [f["name"] for f in self.job_config["filter_repo"] if f["enable"]]

    def do_repo_job(self, repo):
        pass

    def do_fmw_job(self, repo, fmw):
        pass

    def skip_fmw_job(self, repo, fmw):
        pass

    def test_token(self):
        return self.api.test_token()

    def execute(self):
        self.log.write_line({"start at": datetime.now()})
        try:
            repos = [r for r in self.api.list_repos() if r in self.repo_filters]
            for repo in repos:
                self.do_repo_job(repo)
                repo_name = repo["name"],
                fmw_list = self.api.list_repo_fmws(repo_name)
                for fmw in fmw_list:
                    fmw_filter = FMWFilter(self.secret_config_name, self.job_config_name, repo_name, fmw["name"])
                    if not fmw_filter.execute():
                        self.skip_fmw_job(repo, fmw)
                        continue
                    self.do_fmw_job(repo, fmw)
        except APIException as e:
            self.log.write_line(e.error["message"])
            raise e

    def enumerate_fmw(self):
        fmws = FMWCollectionServer(self.secret_config_name, self.job_config_name)
        for fmw in fmws:
            if fmw["valid"]:
                self.do_fmw_job(fmw["repo"], fmw["fmw"])
            else:
                self.skip_fmw_job(fmw["repo"], fmw["fmw"])
