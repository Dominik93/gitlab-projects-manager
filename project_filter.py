def filter_projects(projects, excluded, included):
    filtered_projects = exclude_projects(projects, excluded)
    filtered_projects = include_projects(filtered_projects, included)
    return filtered_projects


def exclude_projects(projects, excluded):
    if excluded is None:
        return projects

    filtered_projects = []
    for project in projects:
        if not _match(excluded, project):
            filtered_projects.append(project)
    return filtered_projects


def include_projects(projects, included):
    if included is None:
        return projects

    filtered_projects = []
    for project in projects:
        if _match(included, project):
            filtered_projects.append(project)
    return filtered_projects


def _match(conditions, project):
    include = []
    for key in conditions:
        for item in conditions[key]:
            include.append(item in str(project[key]))
    return any(include)
