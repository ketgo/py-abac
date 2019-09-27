"""
    Fast json path parser
"""

from jsonpath_ng import parse


class Parser(object):

    def __init__(self, path):
        self.path = parse(path)

    def find(self, json):
        """
            Find value from given JSON at the configured json path. If
            path not found then return `None`.

            :param json: JSON object of type dict

            :return: values occupied by the json path
        """
        matches = self.path.find(json)
        return [match.value for match in matches] if matches else [None]


def is_json_path(path):
    """
        CHeck if given path is a valid json path format

        :param path: path to check
        :return: True if valid else False
    """
    rvalue = True
    try:
        Parser(path)
    except Exception:
        rvalue = False

    return rvalue


def find_json_path(path, data):
    """
        Find value from given JSON at the configured json path. If path not
        found then return `None`.

        :param path: JSON path string
        :param data: data in JSON format
        :return: values occupied by the json path
    """
    return Parser(path).find(data)
