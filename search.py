import os
import re
from functools import reduce

from commons.countable_processor import CountableProcessor
from commons.logger import log, Level
from commons.optional import Optional, of, empty

EXCLUDED = ['.git']


def text_predicate(text):
    return Predicate(text, None)


def regexp_predicate(regexp):
    return Predicate(None, regexp)


class Predicate:

    def __init__(self, text: list | str = None, regexp: str = None):
        self.text = of(text).map(lambda x: text if isinstance(text, list) else [text])
        self.regexp = of(regexp)

    def test(self, content: str) -> bool | None | Exception:
        if self.text.is_present():
            return any(list(map(lambda x: x in content, self.text.get())))
        if self.regexp.is_present():
            return re.search(self.regexp.get(), content)
        raise Exception("Text and regexp are None")


class SearchConfiguration:

    def __init__(self, text_predicate: Predicate = None, file_predicate: Predicate = None, show_content: bool = None):
        self.text_predicate = of(text_predicate)
        self.file_predicate = of(file_predicate)
        self.show_content = show_content


class Hit:

    def __init__(self, config: SearchConfiguration, content: str):
        self.config = config
        self.content = content

    def get_hit(self, identifier) -> Optional:
        predicate = self.config.text_predicate.get()
        if predicate.test(self.content):
            content = None
            if self.config.show_content:
                content = self._find_line(predicate)
            return of({"identifier": identifier, "content": content})
        return empty()

    def _find_line(self, predicate: Predicate):
        for line in self.content.split("\n"):
            if predicate.test(line):
                return line.strip()
        raise Exception(f"Line with text {predicate} not found in content.")


@log(level=Level.DEBUG, start_message="Search {args}", end_message=None)
def _read(path):
    f = open(path, "r", encoding="utf8")
    file_content = f.read()
    f.close()
    return file_content


def _search_in_project(project_directory: str, config: SearchConfiguration) -> list:
    hits = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        dirnames[:] = _filter_directories(dirnames)
        for file in _filter_files(config, filenames):
            path = dirpath + '/' + file
            Hit(config, _read(path)).get_hit(path).if_present(lambda x: hits.append(x))
    return hits


def _filter_files(config: SearchConfiguration, filenames):
    return config.file_predicate.map(lambda p: list(filter(lambda f: p.test(f), filenames))).or_get(filenames)


def _filter_directories(dirnames):
    return list(filter(lambda x: x not in EXCLUDED, dirnames))


def search(paths: list, config: SearchConfiguration):
    search_results = CountableProcessor(lambda x: _search_in_project(x, config)).run(paths)
    return reduce(list.__add__, search_results, [])
