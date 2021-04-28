from FMEServerWorkspaceJob import FMEServerWorkspaceJob
import sys

sys.path.append('../FMEServerLib')
from FileLogger.Logger import AppLogger
import os
import json

CONFIG = "app.json"

with open(CONFIG) as app_config_json:
    app_config = json.load(app_config_json)
log = AppLogger(os.path.join(app_config["log_dir"], "log.txt"), True, True)

try:
    job = FMEServerWorkspaceJob(log)
    job.run_workspace()
except Exception as e:
    log.write_line(e)
