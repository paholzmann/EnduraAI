const races = [
    {
        rank: 1,
        name: "Pitz Alpine Glacier Trail",
        category: "50K",
        distance: "45 km",
        elevation: "2,800 m+",
        projectedPlace: "Top 8%",
        opportunity: "Very High",
        match: 94
    },
    {
        rank: 2,
        name: "Mozart 100 Scenic",
        category: "100K",
        distance: "81 km",
        elevation: "4,300 m+",
        projectedPlace: "Top 15%",
        opportunity: "High",
        match: 87
    },
    {
        rank: 3,
        name: "Alpen Trail Challenge",
        category: "50K",
        distance: "52 km",
        elevation: "3,100 m+",
        projectedPlace: "Top 20%",
        opportunity: "Medium",
        match: 76
    }
];

const tableBody = document.querySelector("#raceTableBody");
const searchInput = document.querySelector("#raceSearch");
const categoryFilter = document.querySelector("#categoryFilter");

function renderTable(data) {
    tableBody.innerHTML = "";

    data.forEach(race => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>#${race.rank}</td>
            <td class="race-name">${race.name}</td>
            <td><span class="badge">${race.category}</span></td>
            <td>${race.distance}</td>
            <td>${race.elevation}</td>
            <td>${race.projectedPlace}</td>
            <td>${race.opportunity}</td>
            <td>
                <div class="match-bar">
                    <div class="match-fill" style="width: ${race.match}%"></div>
                </div>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

function filterRaces() {
    const searchValue = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;

    const filtered = races.filter(race => {
        const matchesSearch = race.name.toLowerCase().includes(searchValue);
        const matchesCategory =
            selectedCategory === "all" || race.category === selectedCategory;

        return matchesSearch && matchesCategory;
    });

    renderTable(filtered);
}

searchInput.addEventListener("input", filterRaces);
categoryFilter.addEventListener("change", filterRaces);

renderTable(races);