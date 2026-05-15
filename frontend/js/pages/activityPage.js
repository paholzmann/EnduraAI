import { loadGPX } from "../gpx/gpx.js";
import { getActivitySummary } from "../api/activityAPI.js";

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
        </main>
    `
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

            const summary =
                await getActivitySummary(file);

            console.log(summary);

        }
    );
}