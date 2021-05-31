import json
import os
from pathlib import Path

from FMEAPI import FMEAPI
from FMEAPI.ApiException import APIException


class FMEServerAPIJob:

    def __init__(self, secret_config_name, job_config_name, server_name, token):
        with open(secret_config_name) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.job = FMEAPI.FmeApis(server_name, token)
        self.output_dir = self.job_config["output_dir"]
        ok = self.job.check_health()
        if not ok:
            raise Exception("FME Server is not healthy.")

    def list_repos(self):
        repo_list = self.job.list_repos()
        return repo_list

    @staticmethod
    def get_fmw_props(api_method, repo_name, fmw_name):
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

    @staticmethod
    def prop_exists(names, get_prop_act):
        try:
            get_prop_act(*names)
            return True
        except APIException:
            return False

    def repo_exists(self, repo_name):
        return self.prop_exists([repo_name], self.job.get_repo_info)

    def fmw_exists(self, repo_name, fmw_name):
        return self.prop_exists([repo_name, fmw_name], self.job.get_repo_fmw)

    def get_repo_fmw(self, repo_name, fmw_name):
        fmw = self.job.get_repo_fmw(repo_name, fmw_name)
        return fmw

    def populate_prop_file_name(self, names, out_dir):
        if len(names) == 0:
            return None
        if len(names) == 1:
            return os.path.join(self.output_dir, out_dir, names[0])
        if len(names) == 2:
            return os.path.join(self.output_dir, out_dir, names[0], names[1])
        return os.path.join(self.output_dir, out_dir, names[0], names[1], names[2])

    def list_fmw_services(self, repo_name, fmw_name):
        return self.job.list_fmw_services(repo_name, fmw_name)

    def list_fmw_resources(self, repo_name, fmw_name):
        return self.job.list_fmw_resources(repo_name, fmw_name)

    def fmw_resource_exists(self, repo_name, fmw_name, resource_name):
        return self.prop_exists([repo_name, fmw_name, resource_name], self.job.get_fmw_resources_info)

    def list_fmw_parameters(self, repo_name, fmw_name):
        return self.job.list_fmw_parameters(repo_name, fmw_name)

    def get_fmw_parameters_pub_info(self, repo_name, fmw_name, pub_name):
        """Retrieves a published parameter of a workspace."""
        return self.job.get_fmw_parameters_pub_info(repo_name, fmw_name, pub_name)

    def download_prop(self, names, out_dir, overwrite, download_prop_act):
        prop_file = self.populate_prop_file_name(names, out_dir)
        if not overwrite and os.path.exists(prop_file):
            raise APIException("File already exists: %s" % prop_file)
        out_dir = os.path.dirname(prop_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        response = download_prop_act(*names)
        Path(os.path.dirname(prop_file)).mkdir(parents=True, exist_ok=True)
        with open(prop_file, 'wb') as f:
            f.write(response["response"].content)
        return response

    def download_fmw(self, repo_name, fmw_name, out_dir, overwrite=False):
        return self.download_prop([repo_name, fmw_name], out_dir, overwrite, self.job.download_fmw)

    def download_repo(self, repo_name, out_dir):
        fmw_list = self.list_repo_fmws(repo_name)
        for fmw in fmw_list:
            self.download_fmw(repo_name, fmw["name"], out_dir)

    def get_fmw_source_dataset(self, repo_name, fmw_name, dataset_dir):
        return self.job.get_fmw_dataset(repo_name, fmw_name, dataset_dir)

    def get_fmw_dataset_info(self, repo_name, fmw_name, dataset_dir, dataset_name):
        return self.job.get_fmw_dataset_info(repo_name, fmw_name, dataset_dir, dataset_name)

    def list_fmw_datasets_features(self, repo_name, fmw_name, dataset_dir, dataset_name):
        return self.job.list_fmw_datasets_features(repo_name, fmw_name, dataset_dir, dataset_name)

    def get_fmw_datasets_feature_info(self, repo_name, fmw_name, dataset_dir, dataset_name, feature_name):
        return self.job.get_fmw_datasets_feature_info(repo_name, fmw_name, dataset_dir, dataset_name, feature_name)

    def upload_fmw(self, repo_name, fmw_name, file):
        return self.job.upload_fmw(repo_name, fmw_name, file)
