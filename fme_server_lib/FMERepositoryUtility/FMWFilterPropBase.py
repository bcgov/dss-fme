from .FMWFilterSubBase import FMWFilterSubBase


class FMWFilterPropBase(FMWFilterSubBase):

    def __init__(self, job_config_name, api_method, rule):
        super().__init__(job_config_name, "filter_fmw_prop", rule, api_method)

    def pass_single_filter(self, key, sub_filter):
        try:
            props = self.api_method(key)
        except:
            return self.prop_no_method()
        if not props:
            return self.prop_no_method()
        for f in sub_filter[key]:
            if f not in props.keys():
                if not self.prop_no_method():
                    return False
            if not self.prop_yes_method(sub_filter[key], props, f):
                return False
        return True
