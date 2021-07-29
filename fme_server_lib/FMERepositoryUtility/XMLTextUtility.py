from .RegSearch import RegSearch


class XMLTextUtility:

    def __init__(self, text=None, section_end=None):
        self.text = text
        self.section_end = section_end

    def find_sections(self, head, include_cri, exclude_cri):
        search = RegSearch(self.text, self.section_end)
        return search.find_sections(head, include_cri, exclude_cri)

    def find_lines(self, criteria):
        search = RegSearch(self.text)
        return search.find_lines(criteria)

    @staticmethod
    def sub_sections(sections, include_cri, exclude_cri):
        result = list()
        for section in sections:
            search = RegSearch(section.text)
            ok = True
            for inc_cri in include_cri:
                if not search.contain_line(inc_cri):
                    ok = False
            if not ok:
                continue
            for exc_cri in exclude_cri:
                if search.contain_line(exc_cri):
                    ok = False
            if not ok:
                continue
            result.append(section)
        return result
