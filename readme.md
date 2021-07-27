# StateTrace Django

Adds StateTrace annotation functionality to Django applications.


## Installation

```bash
python -m pip install git+https://github.com/SoCal-Software-Labs/statetrace_django
```

In Settings.py add statetrace django to installed apps and middleware.


```python
INSTALLED_APPS = [
    ...,
    'statetrace_django',
]

MIDDLEWARE = [
    ...,
    'statetrace_django.middleware.statetrace_middleware'
]

# Configure the link to the search page:
STATETRACE_SEARCH_URL = "http://my-statetrace-deployment/organizations/1/environments/1/frames?database_id=1"

```

## Metadata

Hooks are provided to extract metadata from request objects:


```python
def action_meta(request):
    return {"my custom action meta": {"arbitary json": request.META["SOME_META"]}}

def session_meta(request):
    return {"my custom session meta": {"some json": 456}}

```

```python
STATETRACE_ACTION_META  = "myapp.statetrace.action_meta"

STATETRACE_SESSION_META = "myapp.statetrace.session_meta"
```


## Choosing which requests to annotate

By default StateTrace annotates all `["POST", "PUT", "DELETE", "PATCH"]` requests. To change this, you can set a special function

```python
BLACKLISTED = [...]
def filter_func(request):
    return request.method in ["POST", "PUT", "DELETE", "PATCH", "GET"] and request.url not in BLACKLISTED

```


```python
STATETRACE_REQUEST_FILTER = "myapp.statetrace.filter_func"
```
