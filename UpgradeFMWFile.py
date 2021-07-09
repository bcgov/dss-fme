import json
import os.path
import os
import re
import shutil

from FMWFile import FMWFile
from FileLogger.Logger import AppLogger


class UpgradeFMWFile:

    def __init__(self, app_config_name, job_config_name):
        with open(app_config_name) as app_config_json:
            self.app_config = json.load(app_config_json)
        with open(job_config_name) as job_config_json:
            self.job_config = json.load(job_config_json)
        self.log = AppLogger(os.path.join(self.app_config["log_dir"], "log.txt"), True, True)

    @staticmethod
    def dataset_to_fix(dataset_name, dest_dataset):
        dataset_sections = FMWFile.filter_section(dest_dataset, [dataset_name], [])
        return len(dataset_sections) > 0

    @staticmethod
    def section_to_fix(text, dest_dataset):
        m = re.search(r'#!\s+IS_SOURCE="false"\s*\n+', text)
        if not m:
            return False
        m = re.search(r'#!\s+FEATURE_TYPE_NAME_QUALIFIER=""\s*\n+', text)
        if not m:
            return False
        m = re.search(r'#!\s+KEYWORD="((?!").)*"\s*\n', text)
        if not m:
            return False
        key = text[m.regs[0][0]: m.regs[0][1]]
        return UpgradeFMWFile.dataset_to_fix(key, dest_dataset)

    def fix_fmw(self, text, dest_dataset):

        def fix(in_text, out_text, changed):
            m = re.search(FMWFile.line_search_cri("<FEATURE_TYPE"), in_text)
            if not m:
                out_text += in_text
                in_text = ""
                return in_text, out_text, changed
            out_text += in_text[:m.regs[0][1]]
            in_text = in_text[m.regs[0][1]:]
            m = re.search(FMWFile.line_search_cri(">"), in_text)
            if not m:
                out_text += in_text
                in_text = ""
                return in_text, out_text, changed
            section = in_text[:m.regs[0][1]]
            if self.section_to_fix(section, dest_dataset):
                section = section.replace('FEATURE_TYPE_NAME_QUALIFIER=""', 'FEATURE_TYPE_NAME_QUALIFIER=" "')
                changed = True
            out_text += section
            in_text = in_text[m.regs[0][1]:]
            return fix(in_text, out_text, changed)

        out_text0 = ""
        changed0 = False
        result = fix(text, out_text0, changed0)
        return result[1], result[2]

    def execute(self, fmw_file_name, fmw_file_name_upgrade):
        fmw_file = FMWFile(fmw_file_name)
        fmw_file.load()
        include_cri = [fmw_file.line_search_cri('FEATURE_TYPE_NAME_QUALIFIER=""'),
                       fmw_file.line_search_cri(r'NODE_NAME="[\w]+\.[\w]+"')]
        exclude_cri = [fmw_file.line_search_cri(r'KEYWORD="CSV[_\d]*"')]
        dest_feature_sections = FMWFile.filter_section(fmw_file.dest_feature_sections, include_cri, exclude_cri)
        include_cri = [FMWFile.line_search_cri('GENERATE_FME_BUILD_NUM="17539"')]
        exclude_cri = [FMWFile.line_search_cri(r'FORMAT="CSV\d*"')]
        dest_dataset_sections = FMWFile.filter_section(fmw_file.dest_dataset_sections, include_cri, exclude_cri)
        if len(dest_feature_sections) == 0 or len(dest_dataset_sections) == 0:
            return
        result = self.fix_fmw(fmw_file.text, dest_dataset_sections)
        if not result[1]:
            return
        out_text = result[0]
        out_dir = os.path.dirname(fmw_file_name_upgrade)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        self.log.write_line(f"Upgrading {fmw_file_name} ...")
        f = open(fmw_file_name_upgrade, "w")
        try:
            f.write(out_text)
        finally:
            f.close()
        shutil.copyfile(f'{fmw_file_name}.service.json', f'{fmw_file_name_upgrade}.service.json')
