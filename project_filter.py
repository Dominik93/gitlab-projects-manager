def filter_projects(projects: list[dict], excluded: dict, included: dict):
    filtered_projects = projects
    filtered_projects = filtered_projects if _should_not_filter(excluded) else (
        _match_projects(filtered_projects, lambda project: not _match(excluded, project)))
    filtered_projects = filtered_projects if _should_not_filter(included) else (
        _match_projects(filtered_projects, lambda project: _match(included, project)))
    return filtered_projects


def _should_not_filter(project_filter: dict):
    return project_filter is None or not project_filter


def _match_projects(projects: list[dict], condition):
    filtered_projects = []
    for project in projects:
        if condition(project):
            filtered_projects.append(project)
    return filtered_projects


def _match(conditions: dict, project: dict):
    include = []
    for key in conditions:
        for item in conditions[key]:
            include.append(item in str(project[key]))
    return any(include)
