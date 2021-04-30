import re


class FMWRepositoryUtil:

    def __init__(self, repo_name, fmw_name):
        self.repo_name = repo_name
        self.fmw_name = fmw_name

    def filter_fmw(self, filters):
        for f in filters:
            if re.search(f, self.fmw_name.lower()):
                return False
        return True
