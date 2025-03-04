import random
from datetime import datetime, timezone

from locust import HttpUser, between, task


class FastAPIUser(HttpUser):
    # Simulate a wait time between tasks (users are simulated to wait a bit between requests)
    host = "http://localhost:8000"  # Host of the FastAPI app
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

    # @task
    # def add_user(self):
    #     # Simulate a POST request to "/api/v1/users/" endpoint
    #     _id = random.randint(1, 10000)
    #     self.client.post("/api/v1/users/", json={"name": f"Shaik Malik Basha - {_id}"})

    @task
    def get_users(self):
        # Simulate a GET request to "/api/v1/users/" endpoint
        self.client.get("/api/v1/users/")


class WebUser(HttpUser):
    # Simulate a wait time between tasks (users are simulated to wait a bit between requests)
    host = "http://localhost:8000"  # Host of the FastAPI app
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

    # @task
    # def add_notes(self):
    #     _id = random.randint(1, 10000)
    #     self.client.post(
    #         "/api/v1/notes/",
    #         json={
    #             "title": f"Notes Title - {_id}",
    #             "description": f"Notes Description - {_id}",
    #             "status": "PENDING",
    #             "target_date": datetime.now(timezone.utc).isoformat(),
    #             "user_id": 0,
    #         },
    #     )

    @task
    def get_notes(self):
        self.client.get("/api/v1/notes/")
