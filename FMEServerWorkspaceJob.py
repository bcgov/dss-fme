import json
import sys
import time
import math

sys.path.append('../FMEServerLib')
from FMERepositoryUtility import FMWParameterUtil
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

    def pass_filter(self, param_util):
        for param in self.job_config["filter_props"]:
            key = list(param.keys())[0]
            try:
                value = param_util.get_parameter(key)
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

    def can_run_workspace(self, workspace):
        strs = workspace.split("/")
        if len(strs) < 2:
            return False
        param_util = FMWParameterUtil.FMWParameterUtil(strs[0].strip(), strs[1].strip(),
                                                       self.job_config["fme_server"],
                                                       self.secret_config["token"])
        return self.pass_filter(param_util)

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

    def filter_can_run(self, fmws):
        chg = False
        for fmw in fmws:
            if fmw["done"]:
                continue
            if not self.can_run_workspace(fmw["name"]):
                fmw["done"] = False
                chg = True
        if chg:
            self.write_result(fmws)

    def run_workspace(self):
        cmd = RunProcess.RunProcess()
        f = open(self.job_config["source_fmw"], "r")
        lines = f.readlines()
        f.close()
        fmws = self.translate(lines)
        if not fmws or len(fmws) == 0:
            return
        # self.filter_can_run(fmws)
        for fmw0 in fmws:
            if fmw0["done"] is not None:
                continue
            fmw = fmw0["name"]
            self.log.write_line(fmw)
            # fmw = "BCGW_SCHEDULED / bcgw_last_table_attributes_bcgw_ora_bcgw.fmw"
            # fmw = "BCGW_SCHEDULED/cbm_intgd_cadastral_fabric_sp_icfprd_sde_idwprod1.fmw"
            cmd_parameters = "%s %s" % (self.server_console, fmw)
            self.log.write_line(cmd_parameters)
            cmd.run(cmd_parameters)
            result = self.parse_result(cmd.result)
            if "status" in result.keys() and result["status"] == "SUCCESS":
                self.log.write_line(result)
                fmw0["done"] = True
            else:
                self.log.write_line("Failed!")
                self.log.write_line(result)
                fmw0["done"] = False
            self.write_result(fmws)
