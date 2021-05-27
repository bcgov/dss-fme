from .FMWFilterSubBase import FMWFilterSubBase


class FMWFilterNameBase(FMWFilterSubBase):

    def __init__(self, job_config_name, rule):
        self.regex = "regex"
        self.text = "text"
        self.method_key = "job_filter_method"
        super().__init__(job_config_name, "filter_fmw_name", rule)

    def pass_regex_filter(self, filter_item):
        pass

    def pass_text_filter(self, filter_item):
        pass

    def pass_single_filter(self, key, sub_filter):
        if key == self.method_key:
            return True
        method = sub_filter[self.method_key]
        if method == self.regex:
            return self.pass_regex_filter(sub_filter[key])
        if method == self.text:
            return self.pass_text_filter(sub_filter[key])
        return True
