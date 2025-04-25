import re

from configuration_reader import read_configuration
from providers.providers_registry import add_provider


@add_provider('domain')
def domain_provider(project):
    domain = find_domain(read_configuration()['domain_regexp'], project["namespace"]["full_path"])
    return domain if domain != '' else project['name']


@add_provider('namespace')
def namespace_provider(project):
    return project['path_with_namespace'].rsplit('/', 1)[0]


@add_provider('ssh')
def ssh_provider(project):
    return project['ssh_url_to_repo']


@add_provider('url')
def url_provider(project):
    return project['web_url']


def find_domain(regexp: str, path: str):
    search = re.search(regexp, path)
    if search is None:
        return ''
    return search.group(1)
