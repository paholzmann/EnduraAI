const form = document.getElementById("race-effort-form");
const resultText = document.getElementById("result-text");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const distanceKm = Number(document.getElementById("distance_km").value);
    const elevationGain = Number(document.getElementById("elevation_gain").value);

    const payload = {
        distance: distanceKm,
        elevation: elevationGain
    };

    try {
        resultText.textContent = "Calculating...";

        const response = await fetch("http://127.0.0.1:8000/api/v1/performance_metrics/race_effort", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${JSON.stringify(data)}`);
        }

        resultText.textContent = `Race effort: ${data.result}`;
    } catch (error) {
        console.error(error);
        resultText.textContent = "Error while calculating race effort";
    }
});