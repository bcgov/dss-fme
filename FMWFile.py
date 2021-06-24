from FMERepositoryUtility.XMLTextUtility import XMLTextUtility


class FMWFile:

    def __init__(self, fmw_name):
        self.fmw_name = fmw_name
        self.text = ""
        self.source_feature_sections = None
        self.dest_feature_sections = None
        self.source_dataset_sections = None
        self.dest_dataset_sections = None

    @staticmethod
    def line_search_cri(text):
        return r'#!\s+' + text + r'\s*\n+'

    def parse(self):
        search = XMLTextUtility(self.text, FMWFile.line_search_cri('>'))
        self.dest_feature_sections = search.find_sections(
            FMWFile.line_search_cri('<FEATURE_TYPE'), [FMWFile.line_search_cri('IS_SOURCE="false"')],
            [FMWFile.line_search_cri('IS_SOURCE="true"')])
        self.source_feature_sections = search.find_sections(
            FMWFile.line_search_cri('<FEATURE_TYPE'), [FMWFile.line_search_cri('IS_SOURCE="true"')],
            [FMWFile.line_search_cri('IS_SOURCE="false"')])
        self.dest_dataset_sections = search.find_sections(
            FMWFile.line_search_cri('<DATASET'), [FMWFile.line_search_cri('IS_SOURCE="false"')],
            [FMWFile.line_search_cri('IS_SOURCE="true"')])
        self.source_dataset_sections = search.find_sections(
            FMWFile.line_search_cri('<DATASET'), [FMWFile.line_search_cri('IS_SOURCE="true"')],
            [FMWFile.line_search_cri('IS_SOURCE="false"')])

    @staticmethod
    def filter_section(sections, include_cri, exclude_cri):
        search = XMLTextUtility()
        return search.sub_sections(sections, include_cri, exclude_cri)

    def load(self):
        f = open(self.fmw_name, "r")
        try:
            self.text = f.read()
        finally:
            f.close()
        self.parse()
