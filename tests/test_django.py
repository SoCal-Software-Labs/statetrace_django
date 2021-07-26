import pytest


@pytest.mark.django_db
def test_tracestate_query(client):
    resp = client.get("/query_model/")
    assert resp.status_code == 200
