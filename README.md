# Gitlab Projects Manager

## Configuration

Change name of `config.json.sample` to `config.json` and provide url to gitlab, your token, group id of space in gitlab,
providers you want to use and other specific configuration.

```json
{
  "gitlab_url": "https://gitlab",
  "access_token": "",
  "group_id": "123",
  "providers": ["domain", "url", "ssh"],
  "provider_specific_configuration": ""
}
```

## Usage

```commandline
python gitlab_projects_manager.py
```

## Customization

Customize your options with [providers_impl.py](providers_implementation%2Fproviders_impl.py). 
Register own provider via decorator

```python
@add_provider('sample')
def sample_provider(project):
    return # your logic
```

To read configuration use `read_configuration()`.
