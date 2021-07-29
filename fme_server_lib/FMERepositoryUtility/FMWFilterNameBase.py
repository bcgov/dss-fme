from .FMWFilterSubBase import FMWFilterSubBase


class FMWFilterNameBase(FMWFilterSubBase):

    def __init__(self, job_config_name, rule):
        self.regex = "regex"
        self.text = "text"
        super().__init__(job_config_name, "filter_fmw_name", rule)

    def pass_regex_filter(self, filter_item):
        pass

    def pass_text_filter(self, filter_item):
        pass

    def pass_single_filter(self, key, sub_filter):
        # if key == self.method_key:
        #     return True
        for key in sub_filter.keys():
            value = sub_filter[key]
            method = value["method"]
            if method == self.regex:
                return self.pass_regex_filter(value['name'])
            if method == self.text:
                return self.pass_text_filter(value['name'])
            return True
