import count_executor
from configuration_reader import read_configuration
from gitlab_accessor import GitlabAccessor
from providers.providers_registry import providers_registry
from store import load
# import providers, do not remove
from providers_implementation import *


def _process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {}
    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


def process(providers: list[str], pages: list[dict]) -> list[dict]:
    return count_executor.provide_countable(pages, lambda x: _process_project(providers, x))


if __name__ == "__main__":
    configuration = read_configuration()
    accessor = GitlabAccessor(configuration['gitlab_url'], configuration['access_token'])
    projects_pages = accessor.get_all_projects(configuration['group_id'])
    projects = load(lambda: process(configuration['providers'], projects_pages), configuration['group_id'])
    print(projects)
