import json
import os
from datetime import datetime
from FMEAPI.ApiException import APIException
from FMERepositoryUtility.FMEServerAPIJob import FMEServerAPIJob
from FMERepositoryUtility.FMWFilter import FMWFilter
# from FMERepositoryUtility.PropFind import PropFind
from FileLogger.Logger import AppLogger


class FMEServerJob:

    def __init__(self, app_config_name, secret_config_name, job_config_name, result=None):
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
        self.result = result
        self.api = FMEServerAPIJob(secret_config_name, job_config_name, self.job_config["fme_server"],
                                   self.secret_config["token"])
        # self.prop_find = PropFind(self.job_config["match"])
        # self.fmw_found_list = list()

    def do_repo_job(self, repo):
        pass

    def do_fmw_job(self, repo, fmw):
        pass

    def skip_fmw_job(self, repo, fmw):
        pass

    def execute(self):
        self.log.write_line({"start at": datetime.now()})
        try:
            repos = self.api.list_repos()
            for repo in repos:
                repo_name = repo["name"]
                if repo_name not in self.job_config["repo_filter"].keys():
                    continue
                if self.job_config["repo_filter"][repo_name] != "1":
                    continue
                self.do_repo_job(repo)
                fmw_list = self.api.list_repo_fmws(repo_name)
                for fmw in fmw_list:
                    fmw_filter = FMWFilter(self.secret_config_name, self.job_config_name, repo["name"], fmw["name"])
                    if not fmw_filter.execute():
                        self.skip_fmw_job(repo, fmw)
                        continue
                    self.do_fmw_job(repo, fmw)
        except APIException as e:
            self.log.write_line(e.error["message"])
            raise e
