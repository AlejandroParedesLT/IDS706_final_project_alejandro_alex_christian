document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload

        const title = document.getElementById("movie-title").value;

        // Show the loading spinner
        loadingDiv.style.display = "block";
        resultsDiv.innerHTML = ""; // Clear previous results

        fetch(`/search?title=${encodeURIComponent(title)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                // Hide the loading spinner
                loadingDiv.style.display = "none";

                if (data.length > 0) {
                    data.forEach(movie => {
                        const movieDiv = document.createElement("div");
                        movieDiv.innerHTML = `
                            <h3>${movie.title}</h3>
                            <p>Genres: ${movie.genres}</p>
                        `;
                        resultsDiv.appendChild(movieDiv);
                    });
                } else {
                    resultsDiv.innerHTML = "<p>No movies found.</p>";
                }
            })
            .catch(error => {
                // Hide the loading spinner in case of error
                loadingDiv.style.display = "none";
                console.error("Error:", error);
                resultsDiv.innerHTML = "<p>An error occurred. Please try again later.</p>";
            });
    });
});
