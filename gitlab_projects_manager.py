from commons.countable_processor import CountableProcessor
from providers.providers_registry import providers_registry

# import providers, do not remove
from providers_implementation import *


def _process_project(providers: list[str], gitlab_project: dict) -> dict:
    project = {}
    for provider in providers:
        project[provider] = providers_registry[provider](gitlab_project)
    return project


def process(providers: list[str], pages: list[dict]) -> list[dict]:
    return CountableProcessor(lambda x: _process_project(providers, x)).run(pages)
