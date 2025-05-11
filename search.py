import os
import re
from functools import reduce

from configuration_reader import read_configuration
from count_executor import provide_countable
from store import get

EXCLUDED = ['.git']


def _hit(text, regexp, content):
    if text is not None:
        return text in content
    if regexp is not None:
        return re.search(regexp, content)
    return Exception("Text and regexp are None")


def _search_in_project(project_directory: str, text: str = None, regexp: str = None, file_extension: str = None):
    results = []
    for (dirpath, dirnames, filenames) in os.walk(project_directory):
        dirnames[:] = list(filter(lambda x: x not in EXCLUDED, dirnames))
        for file in list(filter(lambda x: file_extension is None or file_extension in x, filenames)):
            path = dirpath + '/' + file
            print(f'Search {path}')
            f = open(path, "r", encoding="utf8")
            file_content = f.read()
            f.close()
            if _hit(text, regexp, file_content):
                results.append(path)
    return results


def search(projects: list, text: str = None, regexp: str = None, file_extension: str = None):
    results = provide_countable(projects, lambda x: _search_in_project(x, text, regexp, file_extension))
    return reduce(list.__add__, results)


if __name__ == "__main__":
    configuration = read_configuration()
    directory = configuration['management']['directory']
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", get(configuration['group_id'])))
    results = search(projects, "", "", "")
    print(*results, sep='\n')
