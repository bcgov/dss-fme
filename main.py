import sys
import os
import json

from DownloadFMWJob import DownloadFMWJob
from UpgradeFMWJob import UpgradeFMWJob
from UploadFMWJob import UploadFMWJob

sys.path.append('../FMEServerLib')
from FileLogger.Logger import AppLogger

APP_CONFIG = "app.json"
SECRET_CONFIG = "secret.json"
JOB_CONFIG = "job.json"

with open(APP_CONFIG) as app_config_json:
    app_config = json.load(app_config_json)
log = AppLogger(os.path.join(app_config["log_dir"], "log.txt"), True, True)

try:
    if "download" in sys.argv:
        job = DownloadFMWJob(APP_CONFIG, SECRET_CONFIG, JOB_CONFIG)
        job.execute()
    if "upgrade" in sys.argv:
        job = UpgradeFMWJob(APP_CONFIG, JOB_CONFIG)
        job.execute()
    if "upload" in sys.argv:
        job = UploadFMWJob(APP_CONFIG, SECRET_CONFIG, JOB_CONFIG)
        job.execute()
except Exception as e:
    log.write_line(e)
