from fastapi import FastAPI
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from commons.configuration_reader import read_configuration
from commons.countable_processor import ExceptionStrategy, CountableProcessor
from commons.logger import get_logger
from commons.optional import of
from commons.store import create_store, Storage
from git_actions import pull
from project_filter import filter_projects
from search import Predicate, SearchConfiguration, search


class Filter(BaseModel):
    projects_ids: list = []


class SearchRequest(BaseModel):
    projects_ids: list = []
    search_text: str = None
    search_regex: str = None
    file_text: str = None
    file_regex: str = None
    show_content: bool = False


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger("GitActionsFastAPI")


@app.get("/namespace/{group_id}/projects", tags=['project'])
async def get_projects(group_id):
    logger.info("get_projects", f"GET projects  {group_id}")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    return projects


@app.post("/namespace/{group_id}/pull", tags=['git actions'])
async def post_pull(group_id, project_filter: Filter):
    logger.info("post_pull", f"POST pull {group_id} {project_filter}")
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    id_filter = {"id": None if len(project_filter.projects_ids) == 0 else project_filter.projects_ids}
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_pull", f"{projects}")
    CountableProcessor(lambda x: pull(config_directory, x), strategy=ExceptionStrategy.PASS).run(projects)


@app.post("/namespace/{group_id}/search", tags=['search'])
async def post_search(group_id, request: SearchRequest):
    logger.info("post_search", f"POST search {group_id} {request}")
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    projects = create_store(Storage.JSON).load(lambda: {}, config.get_value("project.group_id"))
    id_filter = {"id": None if len(request.projects_ids) == 0 else request.projects_ids}
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_search", f"{projects}")
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))

    search_predicate = Predicate(request.search_text, request.search_regex)
    file_predicate = Predicate(of(request.file_text).map(lambda x: x.split(',')).or_get(None), request.file_regex)
    search_configuration = SearchConfiguration(search_predicate, file_predicate, request.show_content)
    return search(projects, search_configuration)
