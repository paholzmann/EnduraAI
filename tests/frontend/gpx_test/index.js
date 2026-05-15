let map;
let routeLayer;
let startMarker;
let endMarker;

initialize();

function initialize() {
    map = L.map("activity-map").setView([47.5, 13.3], 7);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    document
        .getElementById("gpx-file-input")
        .addEventListener("change", loadGPX);

    document
        .getElementById("reset-button")
        .addEventListener("click", resetView);

    setTimeout(() => {
        map.invalidateSize();
    }, 300);
}

async function loadGPX(event) {
    const file = event.target.files[0];
    if (!file) return;

    setStatus("Loading...");

    const text = await file.text();
    const points = parseGPX(text);

    if (points.length < 2) {
        setStatus("Invalid GPX file");
        return;
    }

    const metrics = calculateMetrics(points);

    renderRoute(points);
    updateUI(file, points, metrics);

    setStatus("Route loaded", true);
}

function parseGPX(text) {
    const parser = new DOMParser();
    const xml = parser.parseFromString(text, "application/xml");

    return [...xml.getElementsByTagName("trkpt")]
        .map(point => {
            const elevationElement = point.getElementsByTagName("ele")[0];
            const timeElement = point.getElementsByTagName("time")[0];

            return {
                lat: Number(point.getAttribute("lat")),
                lon: Number(point.getAttribute("lon")),
                elevation: elevationElement ? Number(elevationElement.textContent) : null,
                time: timeElement ? new Date(timeElement.textContent) : null
            };
        })
        .filter(point => !Number.isNaN(point.lat) && !Number.isNaN(point.lon));
}

function renderRoute(points) {
    const coordinates = points.map(point => [point.lat, point.lon]);

    if (routeLayer) map.removeLayer(routeLayer);
    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);

    routeLayer = L.polyline(coordinates, {
        color: "#ffffff",
        weight: 4,
        opacity: 0.9
    }).addTo(map);

    startMarker = L.circleMarker(coordinates[0], {
        radius: 6,
        weight: 2,
        color: "#ffffff",
        fillOpacity: 1
    }).addTo(map);

    endMarker = L.circleMarker(coordinates[coordinates.length - 1], {
        radius: 6,
        weight: 2,
        color: "#ffffff",
        fillOpacity: 0.5
    }).addTo(map);

    map.fitBounds(routeLayer.getBounds(), {
        padding: [36, 36]
    });
}

function calculateMetrics(points) {
    const distanceKm = calculateDistance(points);
    const elevationStats = calculateElevation(points);
    const durationMs = calculateDuration(points);

    const avgSpeed = durationMs
        ? distanceKm / (durationMs / 3600000)
        : null;

    const avgPace = durationMs && distanceKm > 0
        ? durationMs / 60000 / distanceKm
        : null;

    const verticalRatio = distanceKm > 0
        ? elevationStats.gain / distanceKm
        : 0;

    const raceEffort = distanceKm + elevationStats.gain / 100;

    return {
        distanceKm,
        durationMs,
        avgSpeed,
        avgPace,
        verticalRatio,
        raceEffort,
        ...elevationStats
    };
}

function calculateDistance(points) {
    let distance = 0;

    for (let i = 1; i < points.length; i++) {
        distance += map.distance(
            [points[i - 1].lat, points[i - 1].lon],
            [points[i].lat, points[i].lon]
        );
    }

    return distance / 1000;
}

function calculateElevation(points) {
    let gain = 0;
    let loss = 0;

    const elevations = points
        .map(point => point.elevation)
        .filter(elevation => elevation !== null && !Number.isNaN(elevation));

    for (let i = 1; i < points.length; i++) {
        const previous = points[i - 1].elevation;
        const current = points[i].elevation;

        if (previous === null || current === null) continue;

        const difference = current - previous;

        if (difference > 0) gain += difference;
        if (difference < 0) loss += Math.abs(difference);
    }

    return {
        gain,
        loss,
        minElevation: elevations.length ? Math.min(...elevations) : null,
        maxElevation: elevations.length ? Math.max(...elevations) : null
    };
}

function calculateDuration(points) {
    const times = points
        .map(point => point.time)
        .filter(time => time instanceof Date && !Number.isNaN(time));

    if (times.length < 2) return null;

    return times[times.length - 1] - times[0];
}

function updateUI(file, points, metrics) {
    setText("activity-name", file.name.replace(".gpx", ""));
    setText("activity-summary", createSummary(metrics));

    setText("file-name", file.name);
    setText("distance", metrics.distanceKm.toFixed(2));
    setText("elevation-gain", Math.round(metrics.gain));
    setText("elevation-loss", Math.round(metrics.loss));
    setText("duration", metrics.durationMs ? formatDuration(metrics.durationMs) : "--");
    setText("avg-pace", metrics.avgPace ? formatPace(metrics.avgPace) : "--");
    setText("avg-speed", metrics.avgSpeed ? metrics.avgSpeed.toFixed(1) : "--");
    setText("max-elevation", metrics.maxElevation !== null ? Math.round(metrics.maxElevation) : "--");
    setText("min-elevation", metrics.minElevation !== null ? Math.round(metrics.minElevation) : "--");
    setText("vertical-ratio", Math.round(metrics.verticalRatio));
    setText("points", points.length);
    setText("race-effort", metrics.raceEffort.toFixed(1));
    setText("difficulty", getDifficulty(metrics.raceEffort));

    setText("start-time", points[0].time ? formatDate(points[0].time) : "--");
    setText("end-time", points[points.length - 1].time ? formatDate(points[points.length - 1].time) : "--");

    setText("start-location", formatCoordinates(points[0]));
    setText("end-location", formatCoordinates(points[points.length - 1]));

    setText("route-category", getDistanceCategory(metrics.distanceKm));
    setText("climbing-load", getClimbingLoad(metrics.verticalRatio));
    setText("profile-type", getProfileType(metrics.gain, metrics.loss));
}

function createSummary(metrics) {
    return `${metrics.distanceKm.toFixed(1)} km · ${Math.round(metrics.gain)} m+ · ${metrics.durationMs ? formatDuration(metrics.durationMs) : "no time data"}`;
}

function getDifficulty(raceEffort) {
    if (raceEffort < 15) return "Easy";
    if (raceEffort < 35) return "Moderate";
    if (raceEffort < 70) return "Hard";
    if (raceEffort < 120) return "Ultra";
    return "Extreme";
}

function getDistanceCategory(distanceKm) {
    if (distanceKm < 10) return "Short";
    if (distanceKm < 25) return "Medium";
    if (distanceKm < 45) return "Long";
    if (distanceKm < 80) return "Ultra";
    return "Extreme Ultra";
}

function getClimbingLoad(verticalRatio) {
    if (verticalRatio < 20) return "Flat";
    if (verticalRatio < 45) return "Rolling";
    if (verticalRatio < 80) return "Hilly";
    if (verticalRatio < 120) return "Mountainous";
    return "Extreme";
}

function getProfileType(gain, loss) {
    const difference = Math.abs(gain - loss);

    if (difference < 100) return "Loop / Balanced";
    if (gain > loss) return "Uphill Dominant";
    return "Downhill Dominant";
}

function formatDuration(ms) {
    const totalMinutes = Math.floor(ms / 60000);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    return `${hours}:${String(minutes).padStart(2, "0")}h`;
}

function formatPace(minutesPerKm) {
    const minutes = Math.floor(minutesPerKm);
    const seconds = Math.round((minutesPerKm - minutes) * 60);

    return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

function formatDate(date) {
    return date.toLocaleString("de-DE", {
        day: "2-digit",
        month: "2-digit",
        year: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function formatCoordinates(point) {
    return `${point.lat.toFixed(4)}, ${point.lon.toFixed(4)}`;
}

function setText(id, value) {
    document.getElementById(id).textContent = value;
}

function setStatus(text, loaded = false) {
    document.getElementById("gpx-status-text").textContent = text;

    const status = document.querySelector(".gpx-status");

    if (loaded) {
        status.classList.add("is-loaded");
    } else {
        status.classList.remove("is-loaded");
    }
}

function resetView() {
    if (routeLayer) map.removeLayer(routeLayer);
    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);

    map.setView([47.5, 13.3], 7);

    location.reload();
}