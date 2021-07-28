# Statetrace Django

Adds Statetrace annotation functionality to Django applications.


## Installation

```bash
python -m pip install git+https://github.com/SoCal-Software-Labs/statetrace_django
```

In Settings.py add statetrace django to installed apps and middleware. Make sure to make it the last entry in both lists.


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
    return {"my custom session meta": 456}

```

```python
STATETRACE_ACTION_META  = "myapp.statetrace.action_meta"
STATETRACE_SESSION_META = "myapp.statetrace.session_meta"
```


## Choosing which requests to annotate

By default Statetrace annotates all `["POST", "PUT", "DELETE", "PATCH"]` requests. To change this, you can set a special function

```python
BLACKLISTED = [...]
def filter_func(request):
    return request.method in ["POST", "PUT", "DELETE", "PATCH", "GET"] and request.url not in BLACKLISTED

```


```python
STATETRACE_REQUEST_FILTER = "myapp.statetrace.filter_func"
```


## Setting up Application Identifiers
Setting these variables will help you identify the point in your code when the tranaction happened

```python
STATETRACE_APPLICATION_ID = "git@github.com:our_org/our-prod-app.git" # Identify the code base
STATETRACE_APPLICATION_VERSION = "1.0" # Should be a git tag or commit to identify the point in code
```


## Docker Compose

Use Statetrace with Docker Compose and Django using the following template:

```yaml
version: '3'
    
services:
  web:
    build: .
    command: bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

    command:
      - "postgres"
      - "-c"
      - "wal_level=logical"
      - "-c"
      - "max_wal_senders=1"
      - "-c"
      - "max_replication_slots=2"
      - "-p"
      - "5433"
  
  statetrace:
    image: statetraceofficial/statetrace-beta
    environment:
      - DATABASE_URL=postgres://postgres:postgres@statetrace_db:5432/postgres
      - SECRET_KEY_BASE=123456789123456789123456789123456789123456789123456789123456789123456789
      - STATETRACE_DEMO_MODE=1
      - PORT=9999
    depends_on:
      - statetrace_db
      - db
    ports:
      - "9999:9999"

  statetrace_db:
    image: postgres
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
```

Then using `db` as the host when setting up the Statetrace connection

![Screenshot from 2021-07-28 10-28-17](https://user-images.githubusercontent.com/496914/127368963-f0dfdab6-690b-4c47-849b-c5de0f6da006.png)
