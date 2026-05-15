export function activityPage() {
    return `
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
    `
}

export function initActivityPage() {
    const map = L.map("activity-map").setView([47.7, 13.4],9);
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }
    ).addTo(map)
}