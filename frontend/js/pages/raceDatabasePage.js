import { getRaceDatabase } from "../api/raceDatabaseAPI.js";
import { loadRaceDatabasePage, loadRacePage, renderRaceDatabaseTable } from "../ui/table.js";

export function raceDatabasePage () {
    return `
        <header class="topbar">
            <div class="topbar-left">
                <p class="eyebrow">Dashboard</p>
                <h1 class="page-title">Performance Overview</h1>
            </div>
            <div class="topbar-right">
                <button class="button button-secondary" type="button">Import Race</button>
                <button class="button button-primary">New Analysis</button>
            </div>
        </header>
        <main class="dashboard-main" id="app-main">
            <section class="dashboard-section">
                <div class="section-header">
                    <div>
                        <p class="eyebrow">Race Database</p>
                        <h1 id="race-database-title" class="section-title">Find races you like.</h1>
                    </div>
                </div>
            </section>
            
            <section class="dashboard-section">
                <div class="table-toolbar">
                    <input id="race-database-search" type="search" placeholder="Search...">
                    <select class="category-filter">
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
                                <th>Index</th>
                                <th>Race</th>
                                <th>Date</th>
                                <th>Category</th>
                                <th>Distance</th>
                                <th>Elevation</th>
                                <th>Participants</th>
                                <th>Effort</th>
                            </tr>
                        </thead>
                        <tbody id="race-database-table"></tbody>
                    </table>
                    <div class="pagination">
                        <button class="button button-primary" id="race-database-prev-btn">Previous</button>
                        <button class="button button-primary" id="race-database-next-btn">Next</button>
                    </div>
                </div>
            </section>
        </main>
    `;
}

export async function initRaceDatabasePage () {
    let currentPage = 1;
    const limit = 10;
    let hasNextPage = false;

    const raceDatabaseTable = document.querySelector("#race-database-table");

    const result = await loadRaceDatabasePage(currentPage, limit, raceDatabaseTable);
    currentPage = result.currentPage;
    hasNextPage = result.hasNextPage;

    document.querySelector("#race-database-prev-btn").addEventListener("click", async () => {
        if (currentPage <= 1) return;

        const result = await loadRaceDatabasePage(currentPage - 1, limit, raceDatabaseTable);

        currentPage = result.currentPage;
        hasNextPage = result.hasNextPage;
    });

    document.querySelector("#race-database-next-btn").addEventListener("click", async () => {
        if (!hasNextPage) return;

        const result = await loadRaceDatabasePage(currentPage + 1, limit, raceDatabaseTable);

        currentPage = result.currentPage;
        hasNextPage = result.hasNextPage;
    });
}