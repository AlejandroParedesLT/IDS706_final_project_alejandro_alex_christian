import os
import requests
import pandas as pd


def clean_and_unpivot(df):
    """
    Cleans the DataFrame to remove problematic characters and unpivots
    the genre column.
    """
    # Clean problematic characters
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r"[^\x00-\x7F]+", "", regex=True)
        df[col] = df[col].str.strip()  # Remove extra spaces

    # Unpivot the 'genre' column
    df["genre"] = df["genre"].str.split("|")  # Split genres into lists
    unpivoted_df = df.explode("genre").reset_index(drop=True)  # Explode

    return unpivoted_df


def extract(
    url=(
        "https://github.com/mohammedalawami/Movielens-Dataset/raw/"
        "master/datasets/movies.dat"
    ),
    unpivoted_file_path="data/movies_unpivoted.csv",
    temp_file_path="data/temp_movies.dat",
    timeout=10,
    encoding="latin1",  # Encoding that can handle non-UTF-8 characters
):
    """
    Extracts a dataset from a URL, processes it (cleaning and unpivoting),
    and saves it as a CSV file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(unpivoted_file_path), exist_ok=True)

    # Download the file from the URL
    with requests.get(url, timeout=timeout) as r:
        r.raise_for_status()  # Raise error for bad HTTP responses
        with open(temp_file_path, "wb") as f:
            f.write(r.content)

    try:
        # Load the data into a pandas DataFrame
        df = pd.read_csv(
            temp_file_path, sep="::", header=None, engine="python", encoding=encoding
        )
        df.columns = ["id", "title", "genre"]  # Adjust column names

        # Clean and unpivot the DataFrame
        unpivoted_df = clean_and_unpivot(df)

        # Save the cleaned and unpivoted DataFrame as a CSV file
        unpivoted_df.to_csv(unpivoted_file_path, index=False)
        print(f"Data saved as unpivoted CSV at {unpivoted_file_path}")
        print(unpivoted_df.head())  # Display the first 5 rows

        # Remove the temporary .dat file
        os.remove(temp_file_path)

    except Exception as e:
        print(f"Error reading or processing the file: {e}")

    return "success"


# Run the extract function
if __name__ == "__main__":
    extract()
