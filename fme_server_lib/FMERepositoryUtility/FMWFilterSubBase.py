import json


class FMWFilterSubBase:

    def __init__(self, job_config_name, filter_prop_key, rule, api_method=None):
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.enabled_key = "enable"
        self.filter_rule_key = "job_filter_rule"
        self.filter_prop_key = filter_prop_key
        self.rule = rule
        self.api_method = api_method
        self.items = self.filter_items()

    def filter_items(self):
        result = dict()
        props = self.job_config[self.filter_prop_key]
        if not props:
            return result
        for prop in props:
            if prop[self.enabled_key] and prop[self.filter_rule_key] == self.rule:
                for key in prop.keys():
                    if key not in [self.filter_rule_key, self.enabled_key]:
                        result[key] = prop[key]
        return result

    @staticmethod
    def prop_no_method():
        pass

    def prop_yes_method(self, value, prop, key):
        pass

    def pass_filter(self):
        for key in self.items:
            if not self.pass_single_filter(key, self.items):
                return False
        return True

    def pass_single_filter(self, key, sub_filter):
        pass
