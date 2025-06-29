from commons.configuration_manager import read_configuration
from commons.countable_processor import CountableProcessor
from gitlab_accessor import GitlabAccessor
from providers.providers_registry import providers_registry


def _process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {}
    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


def process_pages(providers: list[str], pages: list[dict]) -> list[dict]:
    return CountableProcessor(pages).run(lambda x: _process_project(providers, x))


def process(group_id) -> dict:
    configuration = read_configuration("config")
    accessor = GitlabAccessor(configuration.get_value("git.url"), configuration.get_value("git.access_token"))
    pages = accessor.get_all_projects(group_id)
    providers = configuration.get_value("providers.loader")
    projects = CountableProcessor(pages).run(lambda x: _process_project(providers, x))
    return {"id": group_id, "projects": projects}
