import unittest
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess


class TestAppHomePageLatency(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8080"
    REQUEST_RATES = [50, 100, 200]  # Define request rates to test
    MAX_WORKERS = 50  # Cap the number of threads to prevent system overload
    RETRY_LIMIT = 3  # Number of retries for a failed request

    @classmethod
    def setUpClass(cls):
        # Start Flask app as a subprocess
        cls.flask_process = subprocess.Popen(
            ["python", "backend/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for the server to start
        for _ in range(10):  # Retry for up to 10 seconds
            try:
                response = requests.get(f"{cls.BASE_URL}/")
                if response.status_code == 200:
                    print("Server is up and running!")
                    return
            except requests.ConnectionError:
                time.sleep(1)

        raise Exception("Server failed to start within the timeout period.")

    @classmethod
    def tearDownClass(cls):
        # Terminate the Flask app
        cls.flask_process.terminate()
        cls.flask_process.wait()

    def make_request(self, retry_count=0):
        """
        Makes a GET request to the home page and returns the response time.
        Retries up to RETRY_LIMIT times on failure.
        """
        try:
            start_time = time.time()
            response = requests.get(f"{self.BASE_URL}/")
            end_time = time.time()
            if response.status_code == 200:
                return end_time - start_time
            else:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                )
        except Exception as e:
            if retry_count < self.RETRY_LIMIT:
                return self.make_request(retry_count + 1)
            else:
                print(f"Request failed after {self.RETRY_LIMIT} retries: {e}")
                return float("inf")

    def test_latency_at_different_rates(self):
        """
        Test the average latency of the home page at different request rates.
        """
        results = {}

        for num_requests in self.REQUEST_RATES:
            with self.subTest(requests=num_requests):
                print(f"\nTesting {num_requests} requests...")
                latencies = []
                max_workers = min(self.MAX_WORKERS, num_requests)

                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [
                        executor.submit(self.make_request) for _ in range(num_requests)
                    ]
                    for future in as_completed(futures):
                        try:
                            latencies.append(future.result())
                        except Exception as e:
                            print(f"Error occurred: {e}")

                average_latency = (
                    sum(latencies) / len(latencies) if latencies else float("inf")
                )
                results[num_requests] = average_latency
                print(
                    f"Average latency for {num_requests} requests: {average_latency:.6f} seconds"
                )

                # Optional assertion: check if the average latency is within an acceptable range
                self.assertLess(
                    average_latency,
                    0.5,
                    f"Average latency for {num_requests} requests is too high: {average_latency:.6f} seconds",
                )

        print("\nSummary of results:")
        for rate, latency in results.items():
            print(f"{rate} requests: {latency:.6f} seconds")


if __name__ == "__main__":
    unittest.main()
