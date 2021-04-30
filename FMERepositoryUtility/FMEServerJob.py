from datetime import datetime
from FMEAPI.ApiException import APIException
from FMERepositoryUtility.FMEServerAPIJob import FMEServerAPIJob
from FMERepositoryUtility.PropFind import PropFind


class FMEServerJob:

    def __init__(self, app_config, secrect_config, job_config, log, result):
        self.debug = app_config["run_mode"] == "debug"
        self.job_config = job_config
        self.log = log
        self.result = result
        self.api = FMEServerAPIJob(job_config, secrect_config, self.job_config["output_dir"], log)
        self.prop_find = PropFind(self.job_config["match"])
        self.fmw_found_list=list()

    def do_repo_job(self, repo):
        pass

    def do_fmw_job(self, repo, fmw):
        pass

    def execute(self):
        self.log.write_line({"start at": datetime.now()})
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
                try:
                    self.do_fmw_job(repo, fmw)
                except APIException as e:
                    self.log.write_line(e.error["message"])
                    raise e
