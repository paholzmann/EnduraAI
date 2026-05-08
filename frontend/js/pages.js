const main = document.querySelector("#app-main");
const navLinks = document.querySelectorAll(".nav-link");

const pages = {
    Overview: `
    <section>
        <h1>Dashboard</h1>
    </section>
    `,
    PerformanceMetrics: `
    <section>
        <h1>Performance Metrics</h1>
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

renderPage("Overview");