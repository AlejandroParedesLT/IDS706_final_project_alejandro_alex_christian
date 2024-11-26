from locust import HttpUser, task, between


class AppLoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulates the user wait time between tasks

    @task(2)
    def home_page(self):
        self.client.get("/")

    @task(3)
    def get_movies(self):
        self.client.get("/movies")

    @task(1)
    def get_movie(self):
        movie_id = 1  # Replace with a valid movie_id from your database
        self.client.get(f"/movie/{movie_id}")

    @task(2)
    def search_movies(self):
        self.client.get("/search", params={"title": "Inception"})

    @task(1)
    def by_genre(self):
        self.client.get("/bygenre", params={"genre": "Action"})

    @task(1)
    def classify_genre(self):
        payload = {"text": "An epic adventure about saving the world."}
        self.client.post("/classify", json=payload)


# To execute the test, run Locust in the terminal with the following command:
# locust -f load_test.py --headless --users 100 --spawn-rate 100 --host http://127.0.0.1:5000

# Explanation of parameters:
# --headless: Runs the load test in headless mode (no UI).
# --users 10000: Simulates 10,000 concurrent users.
# --spawn-rate 10000: Spawns 10,000 users per second.
# --host http://127.0.0.1:5000: Specifies the host where your Flask app is running.
