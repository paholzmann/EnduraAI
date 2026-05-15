let map;
let routeLayer;
let startMarker;
let endMarker;

export async function loadGPX(event, map) {
    const file = event.target.files[0];
    if (!file) return;

    console.log("GPX selected:", file.name);

    const text = await file.text();
    const points = parseGPX(text);

    console.log("Points:", points.length);

    if (points.length < 2) {
        console.log("Invalid GPX file");
        return;
    }

    renderRoute(points, map);

    console.log("GPX loaded successfully");
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
function renderRoute(points, map) {
    const coordinates = points.map(point => [point.lat, point.lon]);

    if (routeLayer) map.removeLayer(routeLayer);
    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);

    const routeShadow = L.polyline(coordinates, {
        color: "#000000",
        weight: 8,
        opacity: 0.45
    }).addTo(map);

    routeLayer = L.polyline(coordinates, {
        color: "#00e5ff",
        weight: 4,
        opacity: 0.95,
        lineJoin: "round",
        lineCap: "round"
    }).addTo(map);

    startMarker = L.circleMarker(coordinates[0], {
        radius: 7,
        color: "#00ff88",
        weight: 3,
        fillColor: "#00ff88",
        fillOpacity: 1
    }).addTo(map);

    endMarker = L.circleMarker(coordinates[coordinates.length - 1], {
        radius: 7,
        color: "#ff4d4d",
        weight: 3,
        fillColor: "#ff4d4d",
        fillOpacity: 1
    }).addTo(map);

    startMarker.bindPopup("Start");
    endMarker.bindPopup("Finish");

    map.fitBounds(routeLayer.getBounds(), {
        padding: [36, 36]
    });
}