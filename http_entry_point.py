from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from commons.configuration_reader import read_configuration
from commons.countable_processor import ExceptionStrategy, CountableProcessor
from commons.logger import get_logger
from commons.optional import of
from commons.store import create_store, Storage
from git_actions import pull, clone, status
from gitlab_actions import process
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

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger("HttpEntryPoint")


@app.get('/')
def get_app_angular():
    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)


@app.post("/namespace/{group_id}", tags=['group'], operation_id="loadGroup")
async def post_load_group(group_id):
    logger.info("post_load_group", f"POST {group_id}")
    create_store(Storage.JSON).load(lambda: process(group_id), group_id)


@app.patch("/namespace/{group_id}", tags=['group'], operation_id="reloadGroup")
async def patch_reload_group(group_id):
    logger.info("patch_reload_group", f"PATCH {group_id}")
    store = create_store(Storage.JSON)
    store.delete(group_id)
    store.load(lambda: process(group_id), group_id)


@app.get("/namespace/{group_id}/projects", tags=['projects'], operation_id="getProjects")
async def get_projects(group_id):
    logger.info("get_projects", f"GET projects {group_id}")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    providers = _get_blocked_providers()
    for project in projects:
        for key in providers:
            del project[key]
    return projects


def _get_blocked_providers():
    config = read_configuration("config")
    ui_providers = config.get_value("providers.ui")
    loader_providers = config.get_value("providers.loader")
    blocked_providers = set()
    for provider in loader_providers:
        if provider not in ui_providers:
            blocked_providers.add(provider)
    return blocked_providers


@app.post("/namespace/{group_id}/projects/pull", tags=['projects'], operation_id="pull")
async def post_pull(group_id, project_filter: Filter):
    logger.info("post_pull", f"POST pull {group_id} {project_filter}")
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    id_filter = _get_id_filter(project_filter.projects_ids)
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_pull", f"{projects}")
    CountableProcessor(lambda x: pull(config_directory, x), strategy=ExceptionStrategy.PASS).run(projects)


@app.post("/namespace/{group_id}/projects/clone", tags=['projects'], operation_id="clone")
async def post_clone(group_id, project_filter: Filter):
    logger.info("post_clone", f"POST clone {group_id} {project_filter}")
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    id_filter = _get_id_filter(project_filter.projects_ids)
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_clone", f"{projects}")
    CountableProcessor(lambda x: clone(config_directory, x), strategy=ExceptionStrategy.PASS).run(projects)


@app.post("/namespace/{group_id}/projects/status", tags=['projects'], operation_id="status")
async def post_status(group_id, project_filter: Filter):
    logger.info("post_status", f"POST status {group_id} {project_filter}")
    config = read_configuration("config")
    config_directory = config.get_value("management.directory")
    store = create_store(Storage.JSON)
    projects = store.get(group_id)
    id_filter = _get_id_filter(project_filter.projects_ids)
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_status", f"{projects}")
    CountableProcessor(lambda x: status(config_directory, x), strategy=ExceptionStrategy.PASS).run(projects)


@app.post("/namespace/{group_id}/projects/search", tags=['projects'], operation_id="search")
async def post_search(group_id, request: SearchRequest):
    logger.info("post_search", f"POST search {group_id} {request}")
    config = read_configuration("config")
    directory = config.get_value("management.directory")
    projects = create_store(Storage.JSON).load(lambda: {}, config.get_value("project.group_id"))
    id_filter = _get_id_filter(request.projects_ids)
    projects = filter_projects(projects, {}, id_filter)
    logger.debug("post_search", f"{projects}")
    projects = list(map(lambda x: f"{directory}/{x['namespace']}/{x['name']}", projects))
    search_predicate = Predicate(request.search_text, request.search_regex)
    file_predicate = Predicate(of(request.file_text).map(lambda x: x.split(',')).or_get(None), request.file_regex)
    search_configuration = SearchConfiguration(search_predicate, file_predicate, request.show_content)
    return search(projects, search_configuration)


def _get_id_filter(ids):
    return {} if len(ids) == 0 else {"id": ids}
