import json
import re

from FMERepositoryUtility.FMWParameterUtil import FMWParameterUtil


class FMWFilter:

    def __init__(self, secret_config_name, job_config_name, repo_name, fmw_name):
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.repo_name = repo_name
        self.fmw_name = fmw_name
        self.fmw_param_util = FMWParameterUtil(secret_config_name, job_config_name, repo_name, fmw_name)

    @staticmethod
    def pass_filter(filters, rule, method):
        if not filters:
            return True
        for f in filters:
            if f["job_filter_rule"] != rule:
                continue
            if method(f, rule):
                return False
        return True

    def name_pass(self, filter_item, rule):
        if rule == "include":
            return not re.search(filter_item["name"], self.fmw_name.lower())
        else:
            return re.search(filter_item["name"], self.fmw_name.lower())

    def prop_meet_rule(self, filter_item, rule):
        key = list(filter_item.keys())[0]
        try:
            value = self.fmw_param_util.get_parameter(key)
        except:
            return rule == "include"
        if not value:
            return rule == "include"
        for prop in filter_item[key]:
            if prop not in value.keys():
                return rule == "include"
            if rule == "include":
                # for including, prop not eaqual, return True break comparing
                if value[prop] != filter_item[key][prop]:
                    # print(rule, prop, value[prop], key, filter_item[key][prop])
                    return True
            else:
                # for excluding, prop eaqual, return True break comparing
                if value[prop] == filter_item[key][prop]:
                    # print(rule, prop, value[prop], key, filter_item[key][prop])
                    return True
        return False

    def pass_name(self):
        filter_item = self.job_config["filter_fmw_name"]
        return self.pass_filter(filter_item, "include", self.name_pass) and self.pass_filter(filter_item, "exclude",
                                                                                             self.name_pass)

    def pass_prop(self):
        filter_item = self.job_config["filter_fmw_prop"]
        return self.pass_filter(filter_item, "include", self.prop_meet_rule) and self.pass_filter(filter_item,
                                                                                                  "exclude",
                                                                                                  self.prop_meet_rule)

    def execute(self):
        return self.pass_name() and self.pass_prop()
