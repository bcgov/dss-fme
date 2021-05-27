import json

from .FMWFilterPropBase import FMWFilterPropBase


class FMWFilterExcludeProp(FMWFilterPropBase):

    def __init__(self, job_config_name, filter_method):
        super().__init__(job_config_name, filter_method, "exclude")

    @staticmethod
    def prop_no_method():
        return True

    def prop_yes_method(self, sub_filter, props, key):
        # for excluding, prop eaqual, return False to break comparing
        return sub_filter[key] != props[key]
