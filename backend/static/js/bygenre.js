document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton");
    const genreSelect = document.getElementById("genre");
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    // Event listener for the search button
    searchButton.addEventListener("click", async () => {
        const genre = genreSelect.value.trim();
        if (!genre) {
            resultsDiv.innerHTML = "<p class='text-danger'>Please select a genre.</p>";
            return;
        }

        // Show the loading spinner
        loadingDiv.style.display = "block";
        resultsDiv.innerHTML = ""; // Clear previous results

        try {
            // Fetch movies by genre
            const response = await fetch(`/bygenre?genre=${encodeURIComponent(genre)}`);
            if (!response.ok) {
                throw new Error("Failed to fetch movies.");
            }
            const movies = await response.json();

            // Hide the loading spinner
            loadingDiv.style.display = "none";

            // Update the results
            if (movies.length > 0) {
                const moviesHtml = movies
                    .map(movie => `
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">${movie.title}</h5>
                                <p class="card-text">Genre: ${movie.genres}</p>
                            </div>
                        </div>
                    `)
                    .join("");
                resultsDiv.innerHTML = moviesHtml;
            } else {
                resultsDiv.innerHTML = "<p class='text-warning'>No movies found for the selected genre.</p>";
            }
        } catch (error) {
            // Hide the loading spinner in case of error
            loadingDiv.style.display = "none";
            resultsDiv.innerHTML = `<p class='text-danger'>Error: ${error.message}</p>`;
        }
    });
});
