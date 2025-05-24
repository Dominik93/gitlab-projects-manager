def filter_projects(projects, excluded, included):
    filtered_projects = exclude_projects(projects, excluded)
    filtered_projects = include_projects(projects, included)
    return filtered_projects


def exclude_projects(projects, excluded):
    if excluded is None:
        return projects

    filtered_projects = []
    for project in projects:
        is_excluded = _exclude(excluded, project)
        if not is_excluded:
            filtered_projects.append(project)
    return filtered_projects


def include_projects(projects, included):
    if included is None:
        return projects

    filtered_projects = []
    for project in projects:
        is_included = _include(included, project)
        if is_included:
            filtered_projects.append(project)
    return filtered_projects


def _include(included, project):
    value = True
    for key in included:
        for item in included[key]:
            value = value and item in str(project[key])
    return value


def _exclude(excluded, project):
    value = False
    for key in excluded:
        for item in excluded[key]:
            value = value or item in str(project[key])
    return value
