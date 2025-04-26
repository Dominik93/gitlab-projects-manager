# Gitlab Projects Manager

## Configuration

Change name of `config.json.sample` to `config.json` and provide url to gitlab, your token, group id of space in gitlab,
providers you want to use and other specific configuration.

```json
{
  "gitlab_url": "https://gitlab",
  "access_token": "",
  "group_id": "123",
  "providers": [
    "namespace",
    "url",
    "ssh"
  ],
  "provider_specific_configuration": ""
}
```

## Usage

```commandline
python gitlab_projects_manager.py
```

## Customization

Customize your registered providers in providers_implementation, any file *.py will be scanned.
Register own provider via decorator:

```python
@add_provider('sample')
def sample_provider(project):
    # your logic
    return {} | ""
```

To read configuration use `read_configuration()`.

# Example

config.json

```json
{
  "gitlab_url": "https://gitlab.com",
  "access_token": "__authtoken__",
  "group_id": "1000",
  "providers": [
    "name",
    "archived",
    "domain",
    "url",
    "ssh"
  ]
}
```

Gitlab projects structure:

```text

- company/namespace
    - components
        - sample-component
    - modules
        - sample
            - sample-api
            - sample-module
```

Result:

```json
[
  {
    "archived": "False",
    "namespace": "company/namespace/modules/sample",
    "ssh": "ssh://git@gitlab.com:2222/company/namespace/modules/sample/sample-api.git",
    "url": "https://gitlab.com/company/namespace/modules/sample/sample-api",
    "name": "sample-api"
  },
  {
    "archived": "False",
    "namespace": "company/namespace/modules/sample",
    "ssh": "ssh://git@gitlab.com:2222/company/namespace/modules/sample/sample-module.git",
    "url": "https://gitlab.com/company/namespace/modules/sample/sample-module",
    "name": "sample-module"
  },
  {
    "archived": "False",
    "namespace": "company/namespace/components",
    "ssh": "ssh://git@gitlab.com:2222/company/namespace/components/sample-component.git",
    "url": "https://gitlab.com/company/namespace/components/sample-component",
    "name": "sample-component"
  }
]
```