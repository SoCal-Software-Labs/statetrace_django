import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionstart(session):
    print("session", session)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session):
    print("end session", session)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    print("before hook", pyfuncitem)

    outcome = yield

    print(outcome)
