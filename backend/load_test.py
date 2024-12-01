# # To execute the test, run Locust in the terminal with the following command:
# # locust -f load_test.py --headless --users 100 --spawn-rate 100 --host http://127.0.0.1:5000

# # Explanation of parameters:
# # --headless: Runs the load test in headless mode (no UI).
# # --users 10000: Simulates 10,000 concurrent users.
# # --spawn-rate 10000: Spawns 10,000 users per second.
# # --host http://127.0.0.1:5000: Specifies the host where your Flask app is running.


from locust import HttpUser, task, between


class AppLoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulates the user wait time between tasks

    @task
    def home_page(self):
        self.client.get("/")


# To execute the test, run Locust in the terminal with the following command:
# locust -f load_test.py --headless --users 100 --spawn-rate 10 --host http://127.0.0.1:5000

# Explanation of parameters:
# --headless: Runs the load test in headless mode (no UI).
# --users 100: Simulates 100 concurrent users.
# --
