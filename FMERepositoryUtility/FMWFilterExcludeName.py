import re

from .FMWFilterNameBase import FMWFilterNameBase


class FMWFilterExcludeName(FMWFilterNameBase):

    def __init__(self, job_config_name, fmw_name):
        self.fmw_name = fmw_name.lower()
        super().__init__(job_config_name, "exclude")

    def pass_regex_filter(self, filter_item):
        return not re.search(filter_item, self.fmw_name)

    def pass_text_filter(self, filter_item):
        return filter_item not in self.fmw_name
