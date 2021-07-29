import json
import re

from .FMWFilterExcludeName import FMWFilterExcludeName
from .FMWFilterExcludeProp import FMWFilterExcludeProp
from .FMWFilterIncludeName import FMWFilterIncludeName
from .FMWFilterIncludeProp import FMWFilterIncludeProp
from .FMWParameterUtil import FMWParameterUtil


class FMWFilter:

    def __init__(self, secret_config_name, job_config_name, repo_name, fmw_name):
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.repo_name = repo_name
        self.fmw_name = fmw_name
        self.fmw_param_util = FMWParameterUtil(secret_config_name, job_config_name, repo_name, fmw_name)
        self.filters = [FMWFilterIncludeProp(job_config_name, self.fmw_param_util.get_parameter),
                        FMWFilterExcludeProp(job_config_name, self.fmw_param_util.get_parameter),
                        FMWFilterIncludeName(job_config_name, fmw_name),
                        FMWFilterExcludeName(job_config_name, fmw_name)]

    def execute(self):
        for f in self.filters:
            if not f.pass_filter():
                return False
        return True
