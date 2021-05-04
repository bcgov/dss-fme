import json
import sys
import os
import time
import math

sys.path.append('../FMEServerLib')
from FMERepositoryUtility import FMWParameterUtil
from FMERepositoryUtility import FMWRepositoryUtil
from ProcessUtility import RunProcess


class FMEServerWorkspaceJob:
    CONFIG = "job.json"
    SECRET = "secret.json"

    def __init__(self, log):
        with open(FMEServerWorkspaceJob.CONFIG) as job_config_json:
            self.job_config = json.load(job_config_json)
        with open(FMEServerWorkspaceJob.SECRET) as secret_config_json:
            self.secret_config = json.load(secret_config_json)
        self.log = log
        self.server_console = self.job_config["server_console"]
        self.cmd = RunProcess.RunProcess()

    def pass_filter_fmw(self, repo, fmw):
        repo_util = FMWRepositoryUtil.FMWRepositoryUtil(repo, fmw)
        return repo_util.filter_fmw(self.job_config["filter_fmw"])

    def pass_filter_param(self, repo, fmw):
        param_util = FMWParameterUtil.FMWParameterUtil(repo, fmw,
                                                       self.job_config["fme_server"],
                                                       self.secret_config["token"])
        return param_util.filter_parameter(self.job_config["filter_props"])

    @staticmethod
    def parse_result(text):
        result = {}
        lines = text.decode("utf-8").split("\r\n")
        for line in lines:
            items = line.split("=")
            if len(items) < 2:
                continue
            if items[0] in ["status", "statusMessage", "timeStarted", "timeFinished"]:
                result[items[0]] = items[1]
        return result

    @staticmethod
    def apply_fmw_status(lines, fmw):
        for line in lines:
            existing = json.loads(line)
            if fmw["name"] == existing["name"]:
                fmw["done"] = existing["done"]
                return

    def check_status(self, fmws):
        f = open(self.job_config["run_status"], "r")
        lines = f.readlines()
        f.close()
        result = list()
        for fmw in fmws:
            self.apply_fmw_status(lines, fmw)
            result.append(fmw)
        return result

    def translate(self, lines):
        result = list()
        for line in lines:
            item = dict()
            item["done"] = None
            strs = line.split(",")
            if len(strs) > 0:
                item["name"] = strs[0].strip()
            if len(strs) > 1:
                item["done"] = strs[1] == "SUCCESS"
            result.append(item)
        result = self.check_status(result)
        return result

    def write_result(self, fmws):
        ticks = math.floor(time.time())
        fn = self.job_config["dest_fmw"] % ticks
        f = open(fn, "w")
        for fmw in fmws:
            f.write(json.dumps(fmw))
            f.write("\n")
        f.close()

    def pass_filter(self, repo, fmw):
        return self.pass_filter_fmw(repo, fmw) and self.pass_filter_param(repo, fmw)

    def do_select_fmw(self):
        f = open(self.job_config["source_fmw"], "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            print(line)
            fmw = json.loads(line)
            if fmw["done"] is not None:
                continue
            strs = fmw["name"].split("/")
            if not self.pass_filter(strs[0].strip(), strs[1].strip()):
                continue
            return fmw
        return None

    def do_update_fmw(self, fmw):
        f = open(self.job_config["source_fmw"], "r")
        lines = f.readlines()
        f.close()
        result = list()
        for line in lines:
            item = json.loads(line)
            if item["name"] == fmw["name"]:
                item["done"] = fmw["done"]
            result.append(item)
        f = open(self.job_config["source_fmw"], "w")
        for r in result:
            f.write(json.dumps(r))
            f.write("\n")
        f.close()

    def lock_action(self, act, fmw):
        def lock_and_act():
            f = open(fn, "w")
            try:
                f.write("busy")
                return act(fmw)
            finally:
                f.close()
                os.remove(fn)

        fn = self.job_config["lock_flag"]
        for i in range(10):
            if not os.path.exists(fn):
                return lock_and_act()
            time.sleep(1)
        raise Exception("The lock file is locked.")

    def select_fmw(self):
        def select_fmw_func(fmw):
            return self.do_select_fmw()

        return self.lock_action(select_fmw_func, None)

    def update_fmw(self, fmw):
        def update_fmw_func(fmw2):
            return self.do_update_fmw(fmw2)

        return self.lock_action(update_fmw_func, fmw)

    def run_workspace(self):
        while True:
            fmw = self.select_fmw()
            if not fmw:
                break
            fmw["done"] = "busy"
            self.update_fmw(fmw)
            self.log.write_line(fmw)
            cmd_parameters = "%s %s" % (self.server_console, fmw["name"])
            self.log.write_line(cmd_parameters)
            self.cmd.run(cmd_parameters)
            result = self.parse_result(self.cmd.result)
            if "status" in result.keys() and result["status"] == "SUCCESS":
                self.log.write_line(result)
                fmw["done"] = "true"
            else:
                self.log.write_line("Failed!")
                self.log.write_line(result)
                fmw["done"] = "false"
            self.update_fmw(fmw)
