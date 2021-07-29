import json

from FMEAPI import FMEAPI


class FMWParameterUtil:

    def __init__(self, secret_config_name, job_config_name, repo_name, fmw_name):
        self.repo_name = repo_name
        self.fmw_name = fmw_name
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        with open(secret_config_name) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        self.api = FMEAPI.FmeApis(self.job_config["fme_server"], self.secret_config["token"])

    def get_parameters(self):
        parameters = self.api.list_fmw_parameters(self.repo_name, self.fmw_name)
        return parameters

    def get_parameter(self, name):
        parameter = self.api.get_fmw_parameters_pub_info(self.repo_name, self.fmw_name, name)
        return parameter
