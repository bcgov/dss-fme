import datetime
from datetime import datetime
import os.path
import os

from FMEAPI.ApiException import APIException
from FMERepositoryUtility.FMEServerJob import FMEServerJob


class UploadFMWJob(FMEServerJob):

    def execute(self):
        self.log.write_line({"start at": datetime.now()})
        try:
            input_dir = self.job_config["input_dir"]
            repos = os.listdir(input_dir)
            for repo in repos:
                filenames = os.listdir(os.path.join(input_dir, repo))
                for file_name in filenames:
                    segs = os.path.splitext(file_name)
                    if segs[1] != ".fmw":
                        continue
                    fmw_file = os.path.join(input_dir, repo, file_name)
                    fmw_name = f"{segs[0]}_upgrade{segs[1]}"
                    self.api.upload_fmw(repo, fmw_name, fmw_file)
        except APIException as e:
            self.log.write_line(e.error["message"])
            raise e
