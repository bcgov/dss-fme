import json
import re


class FMWCollection:

    def __init__(self, fmw_filter=None):
        self.repos = self.populate_repos()
        self.repo_index = 0
        self.fmw_index = -1
        self.fmws = list()
        self.fmw_filter = fmw_filter

    def populate_repos(self):
        return list()

    def populate_fmws(self, repo_name):
        return list()

    def fmw_pass_filter(self, repo_name, fmw_name):
        return True

    def __iter__(self):
        return self

    def return_result(self, repo, fmw, ok):
        return {"repo": repo, "fmw": fmw, "valid": ok}

    def fmw_match_filter(self, fmw):
        for f in self.fmw_filter:
            if not re.match(fmw, f):
                return False
        return True

    def filter_fmw(self):
        if not self.fmw_filter:
            return self.fmws
        return [fmw for fmw in self.fmws if self.fmw_match_filter(fmw)]

    def __next__(self):
        if self.repo_index >= len(self.repos):
            raise StopIteration
        repo = self.repos[self.repo_index]
        if self.fmw_index == -1:
            self.fmws = self.populate_fmws(repo)
            self.fmws = self.filter_fmw()
            self.fmw_index = 0
        if self.fmw_index >= len(self.fmws):
            self.repo_index += 1
            self.fmw_index = -1
            return self.__next__()
        fmw = self.fmws[self.fmw_index]
        self.fmw_index += 1
        ok = self.fmw_pass_filter(repo, fmw)
        return self.return_result(repo, fmw, ok)
