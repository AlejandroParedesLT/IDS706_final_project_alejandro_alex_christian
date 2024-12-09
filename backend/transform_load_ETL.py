"""
Transforms and Loads data into the local Databricks database
"""

import csv
import os
from dotenv import load_dotenv
from databricks import sql


# Load the CSV file and insert it into a new Databricks database
def load(dataset="data/movies_unpivoted.csv"):
    """Transforms and Loads data into the local Databricks database"""
    # Read the dataset
    try:
        payload = csv.reader(open(dataset, newline=""), delimiter=",")
        next(payload)  # Skip the header row
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file {dataset} not found.")
    except Exception as e:
        raise Exception(f"Error reading the dataset: {e}")
    print("here 0")
    # Load environment variables
    load_dotenv()
    print("here 1")
    server_hostname = "dbc-c95fb6bf-a65d.cloud.databricks.com"
    http_path = "/sql/1.0/warehouses/2d6f41451e6394c0"
    access_token = os.getenv("DATABRICKS_API_KEY")
    print(server_hostname)
    print(http_path)
    # Validate environment variables
    if not server_hostname or not http_path or not access_token:
        raise ValueError("Environment variables are not properly set in the .env file.")

    print("here 2")
    # Connect to Databricks using credentials from .env
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        with connection.cursor() as cursor:
            print("check")
            # Create the table if it doesn't exist
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS csm87_movies_final 
                   (movie_id INT, title STRING, genres STRING);
                """
            )

            # Check if the table already contains data
            cursor.execute("SELECT COUNT(*) FROM csm87_movies_final")
            result = cursor.fetchone()
            if result and result[0] == 0:  # Table is empty
                print("Table is empty, inserting data...")

                # Build and execute the SQL INSERT query
                string_sql = "INSERT INTO csm87_movies_final VALUES"
                for row in payload:
                    string_sql += f"\n{tuple(row)},"
                string_sql = (
                    string_sql.rstrip(",") + ";"
                )  # Remove trailing comma and add semicolon
                cursor.execute(string_sql)
                print("Data successfully inserted into csm87_movies.")
            else:
                print("Table already contains data. No insertion needed.")

    return "Database loaded or already loaded."


if __name__ == "__main__":
    print(load())
