from fastapi.testclient import TestClient
from arnold.api.api_v1.endpoints.step import router
from arnold.constants import QUERY_RULES

client = TestClient(router)


def test_query_rules():
    response = client.get("/step/query_rules")
    assert response.status_code == 200
    assert response.json() == QUERY_RULES
