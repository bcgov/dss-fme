import os

from FMEAPI import FMEAPI
from FMEAPI.ApiException import APIException
from pathlib import Path


class FMEServerAPIJob:

    def __init__(self, job_config, secrect_config, output_dir, log):
        self.job_config = job_config
        self.job = FMEAPI.FmeApis(job_config["fme_server"], secrect_config["token"], log)
        self.output_dir = output_dir
        ok = self.job.check_health()
        if not ok:
            raise Exception("FME Server is not healthy.")

    def list_repos(self):
        repo_list = self.job.list_repos()
        return repo_list

    def get_fmw_props(self, api_method, repo_name, fmw_name):
        try:
            return api_method(repo_name, fmw_name)
        except APIException as e:
            return e.error

    def list_repo_fmws(self, repo_name, deep=False):
        fmw_list = self.job.list_repo_fmws(repo_name)
        if deep:
            for fmw in fmw_list:
                fmw["datasets"] = self.get_fmw_props(self.job.get_fmw_datasets, repo_name, fmw["name"])
                fmw["parameters"] = self.get_fmw_props(self.job.list_fmw_parameters, repo_name, fmw["name"])
                fmw["resources"] = self.get_fmw_props(self.job.list_fmw_resources, repo_name, fmw["name"])
                fmw["services"] = self.get_fmw_props(self.job.list_fmw_services, repo_name, fmw["name"])
        return fmw_list

    def prop_exists(self, names, get_prop_act):
        try:
            get_prop_act(*names)
            return True
        except APIException:
            return False

    def repo_exists(self, repo_name):
        get_prop_func = lambda repo_name: self.job.get_repo_info(repo_name)
        return self.prop_exists([repo_name], get_prop_func)

    def fmw_exists(self, repo_name, fmw_name):
        get_prop_func = lambda repo_name, fmw_name: self.job.get_repo_fmw(repo_name, fmw_name)
        return self.prop_exists([repo_name, fmw_name], get_prop_func)

    def get_repo_fmw(self, repo_name, fmw_name):
        fmw = self.job.get_repo_fmw(repo_name, fmw_name)
        return fmw

    def populate_prop_file_name(self, names, dir):
        if len(names) == 0:
            return None
        if len(names) == 1:
            return os.path.join(self.output_dir, dir, names[0])
        if len(names) == 2:
            return os.path.join(self.output_dir, dir, names[0], names[1])
        return os.path.join(self.output_dir, dir, names[0], names[1], names[2])

    def list_fmw_services(self, repo_name, fmw_name):
        return self.job.list_fmw_services(repo_name, fmw_name)

    def list_fmw_resources(self, repo_name, fmw_name):
        return self.job.list_fmw_resources(repo_name, fmw_name)

    def fmw_resource_exists(self, repo_name, fmw_name, resource_name):
        get_prop_func = lambda repo_name, fmw_name, resource_name: self.job.get_fmw_resources_info(repo_name, fmw_name,
                                                                                                   resource_name)
        return self.prop_exists([repo_name, fmw_name, resource_name], get_prop_func)

    def list_fmw_parameters(self, repo_name, fmw_name):
        return self.job.list_fmw_parameters(repo_name, fmw_name)

    def get_fmw_parameters_pub_info(self, repo_name, fmw_name, pub_name):
        """Retrieves a published parameter of a workspace."""
        return self.job.get_fmw_parameters_pub_info(repo_name, fmw_name, pub_name)
