document.addEventListener("DOMContentLoaded", () => {
    const sentimentForm = document.getElementById("sentiment-form");
    const sentimentText = document.getElementById("sentiment-text");
    const resultsDiv = document.getElementById("results");
    const loadingDiv = document.getElementById("loading");

    // Event listener for the sentiment form
    sentimentForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent form from submitting normally

        const text = sentimentText.value.trim();
        if (!text) {
            resultsDiv.innerHTML = "<p class='text-danger'>Please enter some text.</p>";
            return;
        }

        // Show the loading spinner
        loadingDiv.style.display = "block";
        resultsDiv.innerHTML = ""; // Clear previous results

        try {
            // Send the text to the classify API
            const response = await fetch('/classify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error("Failed to fetch movies.");
            }

            const movies = await response.json();

            // Hide the loading spinner
            loadingDiv.style.display = "none";

            // Check if movies were returned
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
                resultsDiv.innerHTML = "<p class='text-warning'>No movies found for the classified genre.</p>";
            }
        } catch (error) {
            // Hide the loading spinner if there's an error
            loadingDiv.style.display = "none";
            resultsDiv.innerHTML = `<p class='text-danger'>Error: ${error.message}</p>`;
        }
    });
});
