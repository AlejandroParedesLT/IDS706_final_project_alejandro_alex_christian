import logging
from flask import Flask, request, jsonify, render_template
from data.db_connection import DBConnection
import requests
import os

# from dotenv import load_dotenv


# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose output
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler(),  # Log to console
    ],
)

# Instantiate DBConnection
db = DBConnection()


@app.route("/")
def home():
    app.logger.info("Home route accessed.")
    return render_template("home.html")


@app.route("/<page>")
def render_page(page):
    valid_pages = ["search_page", "bygenre_page"]
    if page in valid_pages:
        app.logger.info(f"{page.capitalize()} route accessed.")
        return render_template(f"{page}.html")
    return render_template("404.html"), 404


@app.route("/movies", methods=["GET"])
def get_movies():
    """
    Fetches a list of all movies.
    """
    app.logger.info("Fetching all movies...")
    try:
        db.connect()  # Establish connection
        query = "SELECT * FROM db_movies.movies LIMIT 100"  # Adjust query as needed
        db.cursor.execute(query)
        result = db.cursor.fetchall()
        columns = [desc[0] for desc in db.cursor.description]
        movies = [dict(zip(columns, row)) for row in result]
        app.logger.info("Movies fetched successfully.")
        return jsonify(movies)
    except Exception as e:
        app.logger.error(f"Error fetching movies: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure connection is closed
        app.logger.info("Database connection closed after fetching movies.")


@app.route("/movie/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    """
    Fetch details of a specific movie by its ID.
    """
    app.logger.info(f"Fetching movie with ID: {movie_id}")
    try:
        db.connect()  # Establish connection
        query = "SELECT * FROM db_movies.movies WHERE movie_id = ?"
        db.cursor.execute(query, (movie_id,))
        result = db.cursor.fetchone()
        if result:
            columns = [desc[0] for desc in db.cursor.description]
            movie = dict(zip(columns, result))
            app.logger.info(f"Movie with ID {movie_id} fetched successfully.")
            return jsonify(movie)
        else:
            app.logger.warning(f"Movie with ID {movie_id} not found.")
            return jsonify({"message": "Movie not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching movie with ID {movie_id}: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure connection is closed
        app.logger.info(
            f"Database connection closed after fetching movie ID: {movie_id}."
        )


@app.route("/search", methods=["GET"])
def search_movies():
    """
    Search for movies by title.
    """
    title = request.args.get("title", "")
    app.logger.info(f"Searching movies with title containing: '{title}'")
    try:
        db.connect()  # Establish connection
        query = "SELECT * FROM db_movies.movies WHERE title LIKE ?"
        db.cursor.execute(query, (f"%{title}%",))
        result = db.cursor.fetchall()
        columns = [desc[0] for desc in db.cursor.description]
        movies = [dict(zip(columns, row)) for row in result]
        app.logger.info(
            f"Movies search completed for title: '{title}'. Found {len(movies)} results."
        )
        return jsonify(movies)
    except Exception as e:
        app.logger.error(f"Error searching for movies with title '{title}': {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure connection is closed
        app.logger.info(
            f"Database connection closed after searching movies with title: '{title}'."
        )


@app.route("/bygenre", methods=["GET"])
def by_genre():
    """
    Search for movies by genre.
    """
    genre = request.args.get("genre", "")
    app.logger.info(f"Searching movies with genre containing: '{genre}'")
    try:
        db.connect()  # Establish connection
        query = "SELECT * FROM db_movies.movies WHERE genres LIKE ?"
        db.cursor.execute(query, (f"%{genre}%",))
        result = db.cursor.fetchall()
        columns = [desc[0] for desc in db.cursor.description]
        movies = [dict(zip(columns, row)) for row in result]
        app.logger.info(
            f"Movies search completed for genre: '{genre}'. Found {len(movies)} results."
        )
        return jsonify(movies)
    except Exception as e:
        app.logger.error(f"Error searching for movies with genre '{genre}': {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure connection is closed
        app.logger.info(
            f"Database connection closed after searching movies with genre: '{genre}'."
        )


@app.route("/classify", methods=["POST"])
def classify_genre():
    """
    Classify input text into a genre using the Gemini API.
    """
    input_data = request.json
    input_text = input_data.get("text", "")
    if not input_text:
        return jsonify({"error": "Input text is required"}), 400

    app.logger.info(f"Classifying input text: {input_text}")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={os.getenv('LLM_API_KEY')}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Based on the sentiment of the input classify the below text in the follow categories and return strictly one category without any other detail (as an API call for sentiment analysis): [Action, Adventure, Animation, Children's, Comedy, Crime]. Input text: {input_text}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        result = response.json()

        # Extract the genre from the response
        genre = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        app.logger.info(f"Classified genre: {genre}")

        try:
            db.connect()  # Establish connection
            query = "SELECT * FROM db_movies.movies WHERE genres LIKE ?"
            db.cursor.execute(query, (f"%{genre}%",))
            result = db.cursor.fetchall()
            columns = [desc[0] for desc in db.cursor.description]
            movies = [dict(zip(columns, row)) for row in result]
            app.logger.info(
                f"Movies search completed for genre: '{genre}'. Found {len(movies)} results."
            )
            return jsonify(movies)
        except Exception as e:
            app.logger.error(f"Error searching for movies with genre '{genre}': {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            db.close()  # Ensure connection is closed
            app.logger.info(
                f"Database connection closed after searching movies with genre: '{genre}'."
            )
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Failed to classify genre"}), 500


if __name__ == "__main__":
    app.logger.info("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=8080)  # host='0.0.0.0', port=8080
