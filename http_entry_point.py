import json
import traceback
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_camelcase import CamelModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from commons.configuration_manager import read_configuration, save_configuration
from commons.countable_processor import ExceptionStrategy
from commons.logger import get_logger
from commons.optional import of

from entry_point import load_namespace_entry_point, pull_entry_point, clone_entry_point, \
    status_entry_point, \
    search_entry_point, create_branch_entry_point, bump_dependency_entry_point, push_entry_point, commit_entry_point, \
    delete_namespace_entry_point, get_namespaces_entry_point, get_namespace_projects_entry_point, \
    get_search_results_entry_point, \
    get_search_result_entry_point
from project_filter import filter_projects, create_id_filter
from search import SearchConfiguration, text_predicate, regexp_predicate

# import providers, do not remove
from providers_implementation import *

class Filter(CamelModel):
    projects_ids: list = []


class AddGroupRequest(CamelModel):
    name: str
    group: str


class CommitReqeust(CamelModel):
    projects_ids: list = []
    message: str


class SearchRequest(CamelModel):
    name: str
    projects_ids: list = []
    search_text: str = None
    search_regex: bool = False
    file_text: str = None
    file_regex: bool = False
    show_content: bool = False


class BumpDependencyRequest(CamelModel):
    projects_ids: list = []
    dependency: str
    version: str


class CreateBranchRequest(CamelModel):
    projects_ids: list = []
    branch: str


logger = get_logger("HttpEntryPoint")
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


@app.get('/')
def get_app_angular():
    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)


@app.get("/config", tags=['config'], operation_id="get_config")
async def get_config():
    try:
        return read_configuration("config", lambda x: x)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/config", tags=['config'], operation_id="save_config")
async def save_config(request: Request):
    try:
        save_configuration("config", json.dumps(await request.json(), indent=2))
    except Exception as e:
        return _internal_server_error(e)


@app.get("/namespace", tags=['namespace'], operation_id="get_namespaces")
async def get_namespaces():
    try:
        return get_namespaces_entry_point()
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace", tags=['namespace'], operation_id="add_namespace")
async def post_add_namespace(request: AddGroupRequest):
    try:
        load_namespace_entry_point(request.name, request.group)
    except Exception as e:
        return _internal_server_error(e)


@app.delete("/namespace/{name}", tags=['namespace'], operation_id="delete_namespace")
async def delete_namespace(name: str):
    try:
        delete_namespace_entry_point(name)
    except Exception as e:
        return _internal_server_error(e)


@app.get("/namespace/{name}", tags=['namespace'], operation_id="get_namespace")
async def get_namespace(name: str):
    try:
        projects = get_namespace_projects_entry_point(name)
        config = read_configuration("config")
        excluded = config.get_value("project.excluded")
        included = config.get_value("project.included")
        projects = filter_projects(projects, excluded, included)
        providers = _get_blocked_providers()
        for project in projects:
            for key in providers:
                if key in project:
                    del project[key]
        return projects
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/push", tags=['git'], operation_id="push")
async def post_push(name: str, project_filter: Filter):
    try:
        push_entry_point(name, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/commit", tags=['git'], operation_id="commit")
async def post_commit(name: str, request: CommitReqeust):
    try:
        commit_entry_point(name, request.message, _get_projects_filters(request.projects_ids),
                           ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/pull", tags=['git'], operation_id="pull")
async def post_pull(name: str, project_filter: Filter):
    try:
        pull_entry_point(name, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/clone", tags=['git'], operation_id="clone")
async def post_clone(name: str, project_filter: Filter):
    try:
        clone_entry_point(name, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/status", tags=['git'], operation_id="status")
async def post_status(name: str, project_filter: Filter):
    try:
        status_entry_point(name, _get_projects_filters(project_filter.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/branch", tags=['git'], operation_id="create_branch")
async def post_create_branch(name: str, request: CreateBranchRequest):
    try:
        return create_branch_entry_point(name, request.branch, _get_projects_filters(request.projects_ids),
                                         ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.get("/namespace/{name}/search", tags=['file'], operation_id="get_search_result")
async def get_search_results(name: str):
    try:
        return get_search_results_entry_point(name)
    except Exception as e:
        return _internal_server_error(e)


@app.get("/namespace/{name}/search/{result}", tags=['file'], operation_id="get_search_results")
async def get_search_result(name: str, result: str):
    try:
        return get_search_result_entry_point(name, result)
    except Exception as e:
        return _internal_server_error(e)


@app.post("/namespace/{name}/search", tags=['file'], operation_id="search")
async def post_search(name: str, request: SearchRequest):
    try:
        search_predicate = (of(request.search_text)
                            .map(lambda x: regexp_predicate(x) if request.search_regex else text_predicate(x))
                            .or_else_throw())
        file_predicate = (of(request.file_text)
                          .map(lambda x: regexp_predicate(x) if request.file_regex else text_predicate(x.split(',')))
                          .or_get(None))
        search_configuration = SearchConfiguration(search_predicate, file_predicate, request.show_content)
        return search_entry_point(name, request.name, _get_projects_filters(request.projects_ids), search_configuration,
                                  ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


@app.patch("/namespace/{name}/bump-dependency", tags=['maven'], operation_id="bump_dependency")
async def patch_bump_dependency(name: str, request: BumpDependencyRequest):
    try:
        bump_dependency_entry_point(name, request.dependency, request.version,
                                    _get_projects_filters(request.projects_ids), ExceptionStrategy.RAISE)
    except Exception as e:
        return _internal_server_error(e)


def _get_projects_filters(ids: list):
    config = read_configuration("config")
    excluded = config.get_value("project.excluded")
    included = config.get_value("project.included")
    return [
        lambda projects: filter_projects(projects, excluded, included),
        lambda projects: filter_projects(projects, {}, create_id_filter(ids))
    ]


def _get_blocked_providers():
    config = read_configuration("config")
    ui_providers = config.get_value("providers.ui")
    loader_providers = config.get_value("providers.loader")
    blocked_providers = set()
    for provider in loader_providers:
        if provider not in ui_providers:
            blocked_providers.add(provider)
    return blocked_providers


def _internal_server_error(e):
    logger.error("Error", f"Error: {traceback.format_exc()}")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
