const main = document.querySelector("#app-main");
const navLinks = document.querySelectorAll(".nav-link");

const pages = {
    Overview: `
    <section>
        <h1>Overview</h1>
    </section>
    `,
    PerformanceMetrics: `
    <section class="dashboard-section">
        <div class="section-header">
            <div>
                <p class="eyebrow">Performance Metrics</p>
                <h1 id="overview-title" class="section-title">Your Endurance Intelligence Hub</h1>
            </div>
        </div>
        <div class="dashboard-grid">
            <article class="card metric-card">
                <p class="eyebrow">Input</p>
                <form id="performance-metrics-form" class="form metric-form">
                    <div class="form-group">
                        <label for="distance">Distance (km)</label>
                        <input type="number" id="distance" name="distance" placeholder="0">
                    </div>
                    <div class="form-group">
                        <label for="elevation">Elevation gain (m+)</label>
                        <input type="number" id="elevation" name="elevation" placeholder="0">
                    </div>
                    <div class="form-group">
                        <label for="total-time">Total time (minutes)</label>
                        <input type="number" id="total-time" name="total-time" placeholder="0">
                    </div>
                    <button class="button button-primary" type="submit">
                        Calculate
                    </button>
                </form>
            </article>
        </div>
    </section>

    <section class="dashboard-section">
        <div class="section-header">
            <div>
                <p class="eyebrow">Basic Metrics</p>
                <h1 id="overview-title" class="section-title">Lorem BLA BLA BLA BLA</h1>
            </div>
            <p class="section-description">
                Analyze running performance, estimate race difficulty and project competitive outcomes.
            </p>
        </div>
        <div class="dashboard-grid dashboard-grid-4">
            <article class="card metric-card">
                <p class="eyebrow">Race Effort</p>
                <p id="race-effort" class="metric-value">—</p>
                <p class="metric-description">Distance and elevation adjusted load.</p>
            </article>
            <article class="card metric-card">
                <p class="eyebrow">Vertical Rate</p>
                <p id="vertical-rate" class="metric-value">—</p>
                <p class="metric-description">Climb intensity across race profiles.</p>
            </article>
            <article class="card metric-card">
                <p class="eyebrow">Pace on flat equivalent</p>
                <p id="pace-on-flat-equivalent" class="metric-value">—</p>
                <p class="metric-description">Empty</p>
            </article>
            <article class="card metric-card">
                <p class="eyebrow">Pace</p>
                <p id="pace" class="metric-value">—</p>
                <p class="metric-description">Model readiness for prediction.</p>
            </article>
        </div>
    </section>

    <section class="dashboard-section">
        <div class="section-header">
            <div>
                <p class="eyebrow">Race Metrics</p>
                <h1 class="section-title">Race Profile</h1>
            </div>
            <p class="section-description">
                Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
            </p>
        </div>
        <div class="dashboard-grid dashboard-grid-3">
            <article class="card metric-card">
                <p class="eyebrow">Race Category</p>
                <p id="race-category" class="metric-value">—</p>
                <p class="metric-description">A</p>
            </article>
            <article class="card metric-card">
                <p class="eyebrow">Race Difficulty</p>
                <div class="percentage-header">
                    <span id="race-difficulty-score" class="percentage-value">—</span>
                </div>
                
                <div class="percentage-track">
                    <div id="race-difficulty-score-fill" class="percentage-fill"></div>
                </div>
            </article>
            <article class="card metric-card">
                <p class="eyebrow">Category Label</p>
                <p id="category-label" class="metric-value">—</p>
                <p class="metric-description">Model readiness for prediction.</p>
            </article>
        </div>
    </section>

    <section class="dasboard-section">
        <div class="section-header">
            <div>
                <p class="eyebrow">Performance Projection</p>
                <h1 class="section-title">Possible Race Placements</h1>
            </div>
            <p class="section-description">
                Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
            </p>
        </div>
    <section>

    <section class="dasboard-section">
        <div class="section-header">
            <div>
                <p class="eyebrow">Performance Projection</p>
                <h1 class="section-title">Effort Based Race Matching</h1>
            </div>
            <p class="section-description">
                Comprehensive insights and performance analysis to better understand, evaluate, and compare endurance race demands.
            </p>
        </div>
        <div class="table-toolbar">
            <input id="race-search" type="search" placeholder="Search...">
            <select id="category-filter">
                <option value="all">All</option>
                <option value="50K">50K</option>
                <option value="100K">100K</option>
                <option value="100M">100M</option>
            </select>
        </div>
        <div class="table-wrapper">
            <table class="race-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Race</th>
                        <th>Category</th>
                        <th>Distance</th>
                        <th>Elevation</th>
                    </tr>
                </thead>
                <tbody id="effort-based-matches-table"></tbody>
            </table>
            <div class="pagination">
                <button class="button button-primary" id="effort-based-matching-prev-page-btn">Previous</button>
                <button class="button button-primary" id="effort-based-matching-next-btn">Next</button>
            </div>
        </div>
    <section>
    `,
    PerformanceProjection: `
    <section>
        <h1>Performance Projection</h1>
    </section>
    `,
    RaceDatabase: `
    <section>
        <h1>Race Database</h1>
    </section>
    `
}

function renderPage(pageName) {
    main.innerHTML = pages[pageName]
    navLinks.forEach(link => {
        link.classList.remove("active");
        if (link.dataset.page === pageName) {
            link.classList.add("active")
        }
    });
}
navLinks.forEach(link => {
    link.addEventListener("click", () => {
        const pageName = link.dataset.page;
        renderPage(pageName);
    });
});

renderPage("PerformanceMetrics");