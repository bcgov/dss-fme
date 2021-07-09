from datetime import datetime

from FMERepositoryUtility.FMEServerJob import FMEServerJob


class DownloadFMWJob(FMEServerJob):

    def skip_fmw_job(self, repo_name, fmw_name):
        full_name = "%s\\%s" % (repo_name, fmw_name)
        self.log.write_line("Skip %s." % full_name)

    def do_fmw_job(self, repo_name, fmw_name):
        full_name = f"{repo_name}\\{fmw_name}"
        self.log.write_line("Downloading %s ..." % full_name)
        result = self.api.download_fmw(repo_name, fmw_name, self.job_config["output_dir"],
                                       self.job_config["download_overwrite"],
                                       self.job_config["download_service"], self.job_config["download_resource"])
        if 'log' in result.keys():
            self.log.write_line(result["log"])

    def execute(self):
        self.log.write_line({"start at": datetime.now()})
        self.enumerate_fmw()
