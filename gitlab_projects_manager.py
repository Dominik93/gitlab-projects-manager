from configuration_reader import read_configuration
from gitlab_accessor import GitlabAccessor
from providers.providers_registry import providers_registry
# import providers, do not remove
from providers_implementation import *


def process(providers: list[str], pages: list[list[dict]]) -> list[dict]:
    projects = []
    for page in pages:
        for project in page:
            projects.append(process_project(providers, project))
    return projects


def process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {}
    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


if __name__ == "__main__":
    configuration = read_configuration()
    accessor = GitlabAccessor(configuration['gitlab_url'], configuration['access_token'])
    projects_pages = accessor.get_all_projects(configuration['group_id'])
    print(process(configuration['providers'], projects_pages))
