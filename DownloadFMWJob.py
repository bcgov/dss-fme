from FMERepositoryUtility.FMEServerJob import FMEServerJob


class DownloadFMWJob(FMEServerJob):

    def skip_fmw_job(self, repo, fmw):
        repo_name = repo["name"]
        fmw_name = fmw["name"]
        full_name = "%s\\%s" % (repo_name, fmw_name)
        self.log.write_line("Skip %s." % full_name)

    def do_fmw_job(self, repo, fmw):
        repo_name = repo["name"]
        fmw_name = fmw["name"]
        full_name = f"{repo_name}\\{fmw_name}"
        self.log.write_line("Downloading %s ..." % full_name)
        self.api.download_fmw(repo_name, fmw_name, self.job_config["output_dir"], self.job_config["download_overwrite"])
