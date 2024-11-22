from databricks import sql
import os
from dotenv import load_dotenv

class DBConnection:
    def __init__(self):
        """Initialize the DBConnection and load environment variables."""
        load_dotenv()  # Load environment variables from .env file
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the Databricks SQL database."""
        try:
            self.connection = sql.connect(
                server_hostname=os.getenv("SERVER_HOSTNAME"),
                http_path=os.getenv("DWH_DB"),
                access_token=os.getenv("ACCESS_TOKEN")  # Load token from environment variables
            )
            self.cursor = self.connection.cursor()
            print("Connected to Databricks SQL database.")
        except Exception as e:
            print(f"Error connecting to Databricks SQL database: {e}")
            raise

    def close(self):
        """Closes the cursor and connection to the Databricks SQL database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")
