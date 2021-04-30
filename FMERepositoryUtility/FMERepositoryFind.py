from FMEAPI.ApiException import APIException
from FMERepositoryUtility.FMEServerJob import FMEServerJob
from FMERepositoryUtility.FMWFind import FMWFind


class FMERepositoryFind(FMEServerJob):

    def do_fmw_job(self, repo, fmw):
        repo_name = repo["name"]
        fmw_name = fmw["name"]
        full_name = "%s\\%s" % (repo_name, fmw_name)
        if self.job_config["fmw_filter"]["on"]:
            if fmw_name not in self.job_config["fmw_filter"]["items"]:
                return
        # self.log.write_line("Finding in %s ..." % full_name)
        parameters = self.api.list_fmw_parameters(repo_name, fmw_name)
        fmw_find = FMWFind(repo_name, fmw_name, parameters, self.prop_find, self.log)
        try:
            fmw_find.find()
            if self.prop_find.found():
                line = "%s/%s" % (repo_name, fmw_name)
                self.fmw_found_list.append(line)
                self.log.write_line(line)
        except APIException as e:
            raise APIException("Error: %s. reason: %s" % (full_name, e.error["message"]))
