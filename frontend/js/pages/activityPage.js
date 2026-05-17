import { loadGPX } from "../gpx/gpx.js";
import { getActivitySummary } from "../api/activityAPI.js";
import { convertMinutesToReadableHours, convertPaceToReadablePace, roundToTwoDecimals, metersPerSecondToKmPerHour } from "../utils/formatter.js";

export function activityPage() {
    return `
        <header class="topbar">
            <div class="topbar-left">
                <p class="eyebrow">Dashboard</p>
                <h1 class="page-title">Performance Overview</h1>
            </div>
            <div class="topbar-right">
                <button id="export-results-btn" class="button button-secondary" type="button">Export Results</button>
                <button id="upload-gpx-btn" class="button button-primary">Upload GPX</button>
                <input id="gpx-file-input" type="file" accept=".gpx" hidden>
            </div>
        </header>
        <main class="dashboard-main" id="app-main">
            <section class="dashboard-section">
                <div class="section-header">
                    <div>
                        <p class="eyebrow">Performance Metrics</p>
                        <h1 id="overview-title" class="section-title">Your Endurance Intelligence Hub</h1>
                    </div>
                </div>
                <div class="dashboard-grid">
                    <article class="card metric-card">
                        <div id="activity-map" class="map"></div>
                    </article>
                </div>
            </section>
            <section class="dashboard-section">
                <div class="section-header">
                    <div>
                        <p class="eyebrow">Basics</p>
                        <h1 class="section-title">Basics</h1>
                    </div>
                    <p class="section-description">
                        Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
                    </p>
                </div>
                <div class="dashboard-grid">
                    <article class="card metric-card">
                        <p class="eyebrow">Category label</p>
                        <p id="category-label" class="metric-value">—</p>
                        <p class="metric-description">Category label description</p>
                    </article>
                </div>
            </section>
            <section class="dashboard-section">
                <div class="section-header">
                    <div>
                        <p class="eyebrow">Basics</p>
                        <h1 class="section-title">Basics</h1>
                    </div>
                    <p class="section-description">
                        Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
                    </p>
                </div>
                <div class="dashboard-grid dashboard-grid-3">
                    <article class="card metric-card">
                        <p class="eyebrow">Total distance</p>
                        <p id="total-distance" class="metric-value">—</p>
                        <p class="metric-description">Distance description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Total time</p>
                        <p id="total-time" class="metric-value">—</p>
                        <p class="metric-description">Total time description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Activity Effort</p>
                        <p id="activity-effort" class="metric-value">—</p>
                        <p class="metric-description">Activity effort description</p>
                    </article>
                </div>
            </section>
            <section class="dashboard-section">
                <div class="section-header">
                    <div>
                        <p class="eyebrow">Elevation</p>
                        <h1 class="section-title">Basics</h1>
                    </div>
                    <p class="section-description">
                        Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
                    </p>
                </div>
                <div class="dashboard-grid dashboard-grid-4">
                    <article class="card metric-card">
                        <p class="eyebrow">Elevation Gain</p>
                        <p id="total-elevation-gain" class="metric-value">—</p>
                        <p class="metric-description">Elevation description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Lowest/ Highest Point</p>
                        <p id="lowest-highest-point" class="metric-value">—</p>
                        <p class="metric-description">Lowest/ highest point description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Vertical Rate</p>
                        <p id="vertical-rate" class="metric-value">—</p>
                        <p class="metric-description">Vertical rate description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Vertical Per Hour</p>
                        <p id="vertical-per-hour" class="metric-value">—</p>
                        <p class="metric-description">Vertical per hour description</p>
                    </article>
                </div>
            </section>
            <section class="dashboard-section">
                <div class="dashboard-grid dashboard-grid-3">
                    <article class="card metric-card">
                        <p class="eyebrow">Pace</p>
                        <p id="pace" class="metric-value">—</p>
                        <p class="metric-description">Pace description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">SAT</p>
                        <p id="sat" class="metric-value">—</p>
                        <p class="metric-description">SAT description</p>
                    </article>
                    <article class="card metric-card">
                        <p class="eyebrow">Max. Speed</p>
                        <p id="max-speed" class="metric-value">—</p>
                        <p class="metric-description">Max speed description</p>
                    </article>
                </div>
            </section>
        </main>
    `
}

function updateUI(summary) {
    const categoryLabel = summary["Category label"];
    const categoryLabelElement = document.querySelector("#category-label");
    categoryLabelElement.textContent = `${categoryLabel}`;

    const totalDistance = roundToTwoDecimals(summary["Total distance"]);
    const totalDistanceElement = document.querySelector("#total-distance");
    totalDistanceElement.textContent = `${totalDistance} km`;

    const activityEffort = roundToTwoDecimals(summary["Race effort"]);
    const activityEffortElement = document.querySelector("#activity-effort");
    activityEffortElement.textContent = `${activityEffort} km`;

    const uphillElevationGain = roundToTwoDecimals(summary["Uphill elevation gain"]);
    const downhillElevationGain = roundToTwoDecimals(summary["Downhill elevation gain"]);
    const totalElevationElement = document.querySelector("#total-elevation-gain");
    totalElevationElement.textContent = `${uphillElevationGain} m+ / ${downhillElevationGain} m-`;

    const verticalRate = roundToTwoDecimals(summary["Vertical rate"]);
    const verticalRateElement = document.querySelector("#vertical-rate");
    verticalRateElement.textContent = `${verticalRate} m+/km`;

    const verticalPerHour = roundToTwoDecimals(summary["Vertical per hour"]);
    const verticalPerHourElement = document.querySelector("#vertical-per-hour");
    verticalPerHourElement.textContent = `${verticalPerHour} m+/h`;

    const lowestPoint = roundToTwoDecimals(summary["Min elevation"]);
    const highestPoint = roundToTwoDecimals(summary["Max elevation"]);
    const lowestHighestPointElement = document.querySelector("#lowest-highest-point");
    lowestHighestPointElement.textContent = `${lowestPoint} / ${highestPoint} m+`;

    const totalTime = convertMinutesToReadableHours(roundToTwoDecimals(summary["Total time"]));
    const totalTimeElement = document.querySelector("#total-time");
    totalTimeElement.textContent = `${totalTime}`;

    const pace = convertPaceToReadablePace(roundToTwoDecimals(summary["Pace"]));
    const paceElement = document.querySelector("#pace");
    paceElement.textContent = `${pace} min/km`;

    const sat = convertPaceToReadablePace(roundToTwoDecimals(summary["SAT"]));
    const satElement = document.querySelector("#sat");
    satElement.textContent = `${sat} min/km`;

    const maxSpeed = metersPerSecondToKmPerHour(roundToTwoDecimals(summary["Max speed"]));
    const maxSpeedElement = document.querySelector("#max-speed");
    maxSpeedElement.textContent = `${maxSpeed} kph`;
}

export function initActivityPage() {
    const exportBtn = document.querySelector("#export-results-btn");
    const uploadBtn = document.querySelector("#upload-gpx-btn");
    const fileInput = document.querySelector("#gpx-file-input");
    const map = L.map("activity-map").setView([0, 0], 2);

    const mapLayers = {
        "Standard": L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution: "&copy; OpenStreetMap contributors"
            }
        ),

        "Terrain": L.tileLayer(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            {
                attribution: "&copy; OpenTopoMap"
            }
        ),

        "Dark": L.tileLayer(
            "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            {
                attribution: "&copy; OpenStreetMap &copy; CARTO"
            }
        )
    };

    mapLayers["Standard"].addTo(map);
    L.control.layers(mapLayers).addTo(map);

    uploadBtn.addEventListener("click", () => {
        fileInput.click();
    });
    fileInput.addEventListener(
        "change",
        async (event) => {

            const file =
                event.target.files[0];

            if (!file) return;

            loadGPX(event, map);

            const response = await getActivitySummary(file);
            const summary = response.summary;
            console.log(summary);
            updateUI(summary);
        }
    );
}