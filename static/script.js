let routeData = [];

document.getElementById("searchBtn").addEventListener("click", async () => {
    const location = document.getElementById("location").value;
    if (!location) return alert("Please enter a destination!");

    // Show loading spinner
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("results").classList.add("hidden");
    document.getElementById("map").classList.add("hidden");

    const res = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location })
    });

    const data = await res.json();

    // Hide loading spinner
    document.getElementById("loading").classList.add("hidden");

    document.getElementById("results").classList.remove("hidden");
    document.getElementById("places").innerText = data.place;
    document.getElementById("plan").innerText = data.plan;
    document.getElementById("cost").innerText = data.cost;

    // Save route for map
    routeData = data.route || [];

    // Show map button popup only if route data available
    if (routeData.length > 0) {
        document.getElementById("mapPopup").classList.remove("hidden");
    }
});

// Open map with Leaflet.js
let map;  // global map instance

function showMap() {
    document.getElementById("map").classList.remove("hidden");

    // Reset map if already exists
    if (map) {
        map.remove();
    }

    // Initialize map
    map = L.map('map').setView([20.5937, 78.9629], 5); // India fallback
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    if (!routeData || routeData.length === 0) {
        alert("No route data available!");
        return;
    }

    const latlngs = [];

    routeData.forEach((point, i) => {
        if (point.coords && point.coords.length === 2) {
            const coords = [point.coords[0], point.coords[1]];
            latlngs.push(coords);

            L.marker(coords)
                .addTo(map)
                .bindPopup(`${i + 1}. ${point.name} (${point.city})`);
        }
    });

    if (latlngs.length > 1) {
        const polyline = L.polyline(latlngs, { color: 'blue' }).addTo(map);
        map.fitBounds(polyline.getBounds());
    } else {
        map.setView(latlngs[0], 10);
    }
}
