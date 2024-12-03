from locust import HttpUser, task, between, events
from locust import LoadTestShape


class AppLoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulates the user wait time between tasks

    @task
    def home_page(self):
        self.client.get("/")


class StepLoadShape(LoadTestShape):
    """
    A step load shape to ramp up users from 1 to 100 in increments.
    Users will increase by 10 every 30 seconds.
    """

    step_time = 30  # Time for each step in seconds
    step_users = 10  # Number of users to add per step
    max_users = 100  # Maximum number of users

    def tick(self):
        run_time = self.get_run_time()

        if run_time > 180:  # Stop the test after 3 minutes (180 seconds)
            return None

        current_step = run_time // self.step_time + 1
        spawn_rate = (
            self.step_users / self.step_time if self.step_time > 0 else 1
        )  # Prevent division by zero
        user_count = int(
            min(current_step * self.step_users, self.max_users)
        )  # Cap at max_users
        return user_count, spawn_rate


# Hook to print stats at the end of the test
@events.quitting.add_listener
def _(environment, **kwargs):
    stats = environment.stats.total
    print("\nBasic Statistics at the end of the test:")
    print(f"Requests: {stats.num_requests}")
    print(f"Failures: {stats.num_failures}")
    print(f"Average Response Time: {stats.avg_response_time} ms")
    print(f"Max Response Time: {stats.max_response_time} ms")
    print(f"Requests per Second: {stats.total_rps}")


# To execute the test, run Locust in the terminal with the following command:
# locust -f load_test.py --csv=../loadtest_results/loadtest --host http://127.0.0.1:8080


# Explanation of parameters:
# --csv=../loadtest_results/loadtest: Generates CSV files with the load test results in the "../loadtest_results" folder with the prefix "loadtest".
# --host http://127.0.0.1:8080: Specifies the host where your Flask app is running.
# Go to http://localhost:8089/ to see the load test in action.
