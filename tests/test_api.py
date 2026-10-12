from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_ping():
    test_app = FastAPI()
    @test_app.get("/ping")
    def ping():
        return "Bot is Alive !!"
    with TestClient(test_app) as client:
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.text == '"Bot is Alive !!"'