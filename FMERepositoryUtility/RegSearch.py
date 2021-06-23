import re

from .TextSection import TextSection


class RegSearch:

    def __init__(self, text, end_tag=None):
        self.text = text
        self.end_tag = end_tag

    @staticmethod
    def __filter(text, filter_include, filter_exclude):
        if filter_include:
            for item in filter_include:
                m = re.search(item, text)
                if not m:
                    return False
        if filter_exclude:
            for item in filter_exclude:
                m = re.search(item, text)
                if m:
                    return False
        return True

    def __fill_sections(self, head, result, include_cri, exclude_cri):
        """ fill in result with text starting with read, meeting include_cri, exclude_cri """
        if len(self.text) == 0:
            return
        m = re.search(head, self.text)
        if not m:
            return
        start_pos = m.regs[0][0]
        self.text = self.text[m.regs[0][1]:]
        if len(self.text) == 0:
            return
        m = re.search(self.end_tag, self.text)
        if m:
            section = self.text[:m.regs[0][0]]
            end_pos = m.regs[0][1]
            if len(section) > 0 and self.__filter(section, include_cri, exclude_cri):
                result.append(TextSection(section, start_pos, end_pos))
            self.text = self.text[m.regs[0][1]:]
            self.__fill_sections(head, result, include_cri, exclude_cri)

    def find_sections(self, head, include_cri, exclude_cri):
        """ return sections meeting, head line, include and exclude criteria """
        result = []
        self.__fill_sections(head, result, include_cri, exclude_cri)
        return result

    def find_lines(self, criteria):
        """ return lines meeting criteria from self.text  """
        return re.findall(criteria, self.text)

    def contain_line(self, criteria):
        """ check if self.text contains a line meeting criteria """
        result = self.find_lines(criteria)
        return len(result) > 0
