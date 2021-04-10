from contextlib import suppress
import json
from types import SimpleNamespace
from urllib.parse import urlparse

from github import Github


class JsonDeserializer(object):
    def __init__(self, data):
        self.json = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    def _to_dict(self, obj):
        """ converts obj from internal namespace representation to dict."""
        if type(obj) is dict:
            res = {}
            for k, v in obj.items():
                res[k] = self._to_dict(v)
            return res
        elif type(obj) is list:
            return [self._to_dict(item) for item in obj]
        elif type(obj) is SimpleNamespace:
            return self._to_dict(vars(obj))
        else:
            return obj

    def get_field_or_none(self, field):
        """
        :param field: string, path to the requested field using dot notation
        :return: requested field value if available, None otherwise
        """
        with suppress(AttributeError, IndexError):
            value = eval(f'self.json.{field}')
            return self._to_dict(value)


def fetch_json_fields_from_github(url, fields):
    """
    :param url: github url to the folder containing json files
    :param fields: array of paths to the requested fields using dot notation
    :return: array of dicts
    """

    token = "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"
    github = Github(token)
    _, org, repo, location = urlparse(url).path.split('/', 3)
    repo = github.get_repo(org + "/" + repo)

    # XXX: fetching files from github takes way too much time, I suspect a throttle from
    # gh side, couldn't find a workaround.
    data = [JsonDeserializer(f.decoded_content) for f in repo.get_contents(location)]
    return [{
        field: d.get_field_or_none(field)
        for field in fields if d.get_field_or_none(field)
        } for d in data
    ]
