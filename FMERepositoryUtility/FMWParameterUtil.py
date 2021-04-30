from FMEAPI import FMEAPI


class FMWParameterUtil:

    def __init__(self, repo_name, fmw_name, server, secrect):
        self.repo_name = repo_name
        self.fmw_name = fmw_name
        self.api = FMEAPI.FmeApis(server, secrect)

    def get_parameters(self):
        parameters = self.api.list_fmw_parameters(self.repo_name, self.fmw_name)
        return parameters

    def get_parameter(self, name):
        parameter = self.api.get_fmw_parameters_pub_info(self.repo_name, self.fmw_name, name)
        return parameter

    def filter_parameter(self, param_filter):
        for param in param_filter:
            key = list(param.keys())[0]
            try:
                value = self.get_parameter(key)
            except:
                return False
            if not value:
                return False
            for prop in param[key]:
                if prop not in value.keys():
                    return False
                if value[prop] != param[key][prop]:
                    return False
        return True
