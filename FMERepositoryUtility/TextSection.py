import re


class TextSection:

    def __init__(self, text, start_pos, end_pos):
        self.text = text
        self.start_pos = start_pos
        self.end_pos = end_pos
