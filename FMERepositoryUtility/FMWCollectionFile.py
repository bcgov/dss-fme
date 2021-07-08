import os
import re

from .FMWCollection import FMWCollection


class FMWCollectionFile(FMWCollection):

    def __init__(self, repo_dir, fmw_filter=None):
        self.repo_dir = repo_dir
        super().__init__(fmw_filter)

    def populate_repos(self):
        return os.listdir(self.repo_dir)

    def populate_fmws(self, repo_name):
        return [f for f in os.listdir(os.path.join(self.repo_dir, repo_name)) if re.match(r'.+\.fmw$', f)]

    def return_result(self, repo, fmw, ok):
        result = super().return_result(repo, fmw, ok)
        result["full_path"] = os.path.join(self.repo_dir, repo, fmw)
        return result
