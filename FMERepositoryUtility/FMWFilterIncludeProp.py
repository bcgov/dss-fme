import json

from .FMWFilterPropBase import FMWFilterPropBase


class FMWFilterIncludeProp(FMWFilterPropBase):

    def __init__(self, job_config_name, filter_method):
        super().__init__(job_config_name, filter_method, "include")

    @staticmethod
    def prop_no_method():
        return False

    def prop_yes_method(self, sub_filter, props, key):
        # for including, prop not eaqual, return False to break comparing
        return sub_filter[key] == props[key]
