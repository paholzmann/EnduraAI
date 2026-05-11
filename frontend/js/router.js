import { overviewPage } from "./pages/overviewPage.js";
import { initPerformanceMetricsPage, performanceMetricsPage } from "./pages/performanceMetricsPage.js";
import { performanceProjectionPage } from "./pages/performanceProjectionPage.js";
import { initRaceDatabasePage, raceDatabasePage } from "./pages/raceDatabasePage.js";


const pages = {
    Overview: overviewPage,
    PerformanceMetrics: performanceMetricsPage,
    PerformanceProjection: performanceProjectionPage,
    RaceDatabase: raceDatabasePage
};

export function initRouter() {
    const main = document.querySelector("#app-main");
    const navLinks = document.querySelectorAll(".nav-link");

    function renderPage(pageName) {
        main.innerHTML = pages[pageName]();
        if (pageName === "PerformanceMetrics") {
            initPerformanceMetricsPage();
        }
        if (pageName === "RaceDatabase") {
            initRaceDatabasePage();
        }
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

    renderPage("RaceDatabase");
}