from past.types import basestring


class PropFind:

    def __init__(self, matches):
        self.matches = matches
        self.search = None

    def clear(self):
        search = list()
        for match in self.matches:
            d = dict()
            d["values"] = match
            d["found"] = False
            d["props"] = []
            search.append(d)
        self.search = search

    def found(self):
        for match in self.search:
            if not match["found"]:
                return False
        return True

    @staticmethod
    def sub_props(props):
        result = dict()
        for key in props:
            if key != "listOptions":
                result[key] = props[key]
        return result

    @staticmethod
    def match_up(prop_value, match_value, criteria):
        if not isinstance(prop_value, basestring):
            return False
        if not isinstance(match_value, basestring):
            return False
        value = prop_value.lower()
        match_value = match_value.lower()
        if criteria == "equal":
            return value == match_value
        return match_value in value

    @staticmethod
    def sub_match(match):
        result = dict()
        for key in match:
            if key != "criteria":
                result[key] = match[key]
        return result

    @staticmethod
    def sub_match_any_prop(props, match, criteria):
        for key in props:
            if PropFind.match_up(props[key], match["*"], criteria):
                return True
        return False

    @staticmethod
    def sub_match_all_prop(props, match, criteria):
        for key in PropFind.sub_match(match):
            if not PropFind.match_up(props[key], match[key], criteria):
                return False
        return True

    @staticmethod
    def sub_match_prop(props, match):
        criteria = None
        if "criteria" in match.keys():
            criteria = match["criteria"]
        if "*" in match.keys():
            return PropFind.sub_match_any_prop(props, match, criteria)
        else:
            return PropFind.sub_match_all_prop(props, match, criteria)

    @staticmethod
    def match_prop(props, match):
        for sub_match in match:
            if not PropFind.sub_match_prop(props, sub_match):
                return False
        return True

    @staticmethod
    def prop_matched(props, matched):
        for m in matched:
            if m["name"] == props["name"] and m["defaultValue"] == props["defaultValue"]:
                return True
        return False

    def find(self, props):
        if "model" not in props.keys() or props["model"] != "string":
            return
        props = PropFind.sub_props(props)
        for match in self.search:
            if self.match_prop(props, match["values"]):
                match["found"] = True
                if not self.prop_matched(props, match["props"]):
                    match["props"].append(props)
