

const performanceMetricsUrl = "http://127.0.0.1:8000/api/v1/performance_metrics/get_all";


const effortBasedRaceMatchingUrl = "http://127.0.0.1:8000/api/v1/performance_projection/effort_based_race_matching";
let effortBasedRaceMatchingcurrentPage = 1;
let effortBasedRaceMatchingPageSize = 10;
let effortBasedRaceMatchingHasNextPage = false;


const performanceBasedRaceMatchingUrl = "http://127.0.0.1:8000/api/v1/performance_projection/race_placement_projection";
let performanceBasedRaceMatchingCurrentPage = 1;
let performanceBasedRaceMatchingPageSize = 10;
let performanceBasedRaceMatchingHasNextPage = false;

const effortBasedRaceMatchingTable = document.querySelector("#effort-based-matches-table");

const form = document.querySelector("#performance-metrics-form");
const distanceInput = document.querySelector("#distance");
const elevationInput = document.querySelector("#elevation");
const totalTimeInput = document.querySelector("#total-time");

async function getAllPerformanceMetrics() {
    const distance = Number(distanceInput.value);
    const elevation = Number(elevationInput.value);
    const totalTime = Number(totalTimeInput.value);
    try {
        const response = await fetch(performanceMetricsUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                distance: distance,
                elevation: elevation,
                total_minutes: totalTime
            })
        });
        if (!response.ok) {
            throw new Error("Request failed");
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error(error);
    }
}

async function getEffortBasedRaceMatching(page = 1) {
    const distance = Number(distanceInput.value);
    const elevation = Number(elevationInput.value);

    const limit = effortBasedRaceMatchingPageSize;
    const offset = (page - 1) * limit;
    try {
        const response = await fetch(effortBasedRaceMatchingUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                distance: distance,
                elevation: elevation,
                limit: limit,
                offset: offset
            })
        });
        if (!response.ok) {
            throw new Error("Request failed");
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error(error);
    }
}


function renderRaceTable(races, tableBody) {
    const offset = (effortBasedRaceMatchingcurrentPage - 1) * effortBasedRaceMatchingPageSize;

    tableBody.innerHTML = races.map((race, index) => `
        <tr>
            <td>#${offset + index + 1}</td>
            <td>${race["Race_Title"]}</td>
            <td>${race["Race_Category"]}</td>
            <td>${race["Distance"]} km</td>
            <td>${race["Elevation_Gain"]} m+</td>
        </tr>
    `).join("");
}

async function loadRacePage(page = 1) {
    try {
        const data = await getEffortBasedRaceMatching(page);

        const races = data.result;

        effortBasedRaceMatchingcurrentPage = page;
        effortBasedRaceMatchingHasNextPage =
            races.length === effortBasedRaceMatchingPageSize;

        renderRaceTable(races, effortBasedRaceMatchingTable);

        document.querySelector("#effort-based-matching-prev-page-btn").disabled =
            effortBasedRaceMatchingcurrentPage <= 1;

        document.querySelector("#effort-based-matching-next-btn").disabled =
            !effortBasedRaceMatchingHasNextPage;

    } catch (error) {
        console.error(error);
    }
}


function convertPaceToReadablePace(pace) {
    const minutes = Math.floor(pace);
    let seconds = Math.round((pace - minutes) * 60);

    if (seconds === 60) {
        seconds = 0;
        minutes += 1;
    }
    return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

function setRaceCategoryTextColor(raceCategoryItem, raceCategory) {
    if (raceCategory == '20K') {
        return "var(--utmb-20k)";
    }
    else if (raceCategory == '50K') {
        return "var(--utmb-50k)"
    }
    else if (raceCategory == '100K') {
        return "var(--utmb-100k)"
    }
    else if (raceCategory == '100M') {
        return "var(--utmb-100m)"
    }
    else {
        return "white";
    }
}

function setPercentageBar(raceDifficultyScoreItem, raceDifficultyScore, raceDifficultyScoreFillItem) {
    const safeValue = Math.max(0, Math.min(100, raceDifficultyScore));
    const finalValue = safeValue.toFixed(2);
    raceDifficultyScoreItem.textContent = finalValue;
    raceDifficultyScoreFillItem.style.width = `${finalValue}%`;
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const performanceMetrics = await getAllPerformanceMetrics();

    const raceEffort = performanceMetrics.results["Race_effort"];
    const pace = convertPaceToReadablePace(performanceMetrics.results["Pace"]);
    const verticalRate = performanceMetrics.results["Vertical_rate"].toFixed(2);
    const paceOnFlatEquivalent = convertPaceToReadablePace(performanceMetrics.results["Pace_on_flat_equivalent"]);
    const raceCategory = performanceMetrics.results["Race_category"];
    const raceDifficultyScore = performanceMetrics.results["Race_difficulty_score"];
    const categoryLabel = performanceMetrics.results["Category_label"];

    const raceEffortItem = document.querySelector("#race-effort");
    raceEffortItem.textContent = `${raceEffort} km`;
    
    const paceItem = document.querySelector("#pace");
    paceItem.textContent = `${pace} min/km`;

    const verticalRateItem = document.querySelector("#vertical-rate");
    verticalRateItem.textContent = `${verticalRate} m+/km`;

    const paceOnFlatEquivalentItem = document.querySelector("#pace-on-flat-equivalent");
    paceOnFlatEquivalentItem.textContent = `${paceOnFlatEquivalent} min/km`;

    const raceCategoryItem = document.querySelector("#race-category");
    raceCategoryItem.textContent = raceCategory;
    raceCategoryItem.style.color = setRaceCategoryTextColor(raceCategoryItem, raceCategory);

    const raceDifficultyScoreItem = document.querySelector("#race-difficulty-score");
    const raceDifficultyScoreFillItem = document.querySelector("#race-difficulty-score-fill");
    setPercentageBar(raceDifficultyScoreItem, raceDifficultyScore, raceDifficultyScoreFillItem);

    const categoryLabelItem = document.querySelector("#category-label");
    categoryLabelItem.textContent = categoryLabel;


    const effortBasedRaceMatching = await getEffortBasedRaceMatching(1);
    renderRaceTable(effortBasedRaceMatching.result, effortBasedRaceMatchingTable);

    await loadRacePage(1);
});

document.querySelector("#effort-based-matching-prev-page-btn")
    .addEventListener("click", () => {
        if (effortBasedRaceMatchingcurrentPage > 1) {
            loadRacePage(effortBasedRaceMatchingcurrentPage - 1);
        }
    });

document.querySelector("#effort-based-matching-next-btn")
    .addEventListener("click", () => {
        if (effortBasedRaceMatchingHasNextPage) {
            loadRacePage(effortBasedRaceMatchingcurrentPage + 1);
        }
    });